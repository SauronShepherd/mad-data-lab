from unittest.mock import patch
import pytest

from fastapi.testclient import TestClient

from server.main import SESSIONS, app
from backend.data.sql_client import SqlAdapterError


def _unlocked_session(client: TestClient) -> str:
    sid = client.post("/api/sessions", json={"case_id": "CASE_0042"}).json()["session_id"]
    SESSIONS[sid]["evidence_entitlements"] = ["SNAPSHOT_IMPACT"]
    return sid


def test_malformed_evidence_is_a_stable_schema_error_without_truth_leak():
    with TestClient(app) as client:
        sid = _unlocked_session(client)
        with patch("server.main.evidence_repository.records", side_effect=ValueError("private columns invalid")):
            response = client.get(f"/api/sessions/{sid}/evidence")
        assert response.status_code == 502
        assert response.json()["error"]["code"] == "EVIDENCE_SCHEMA_MISMATCH"
        assert "private columns" not in response.text
        assert SESSIONS[sid]["completed"] == []


def test_unexpected_evidence_failure_is_data_invariant_error():
    with TestClient(app) as client:
        sid = _unlocked_session(client)
        with patch("server.main.evidence_repository.records", side_effect=RuntimeError("database unavailable")):
            response = client.get(f"/api/sessions/{sid}/evidence")
        assert response.status_code == 503
        assert response.json()["error"]["code"] == "DATA_INVARIANT_FAILED"
        assert response.json()["error"]["retryable"] is True


def test_empty_evidence_result_is_a_safe_schema_error_without_state_commit():
    with TestClient(app) as client:
        sid = _unlocked_session(client)
        with patch("server.main.evidence_repository.records", return_value=[]):
            response = client.get(f"/api/sessions/{sid}/evidence")
        assert response.status_code == 502
        assert response.json()["error"]["code"] == "EVIDENCE_SCHEMA_MISMATCH"
        assert response.json()["error"]["retryable"] is True
        assert response.json()["error"]["request_id"]
        assert SESSIONS[sid]["completed"] == []


@pytest.mark.parametrize(("code", "retryable"), [
    ("WAREHOUSE_PENDING", True),
    ("WAREHOUSE_QUOTA_EXHAUSTED", True),
    ("APP_RESOURCE_UNAVAILABLE", True),
])
def test_sql_platform_error_reaches_http_envelope_without_provider_details(code, retryable):
    with TestClient(app) as client:
        sid = _unlocked_session(client)
        with patch("server.main.evidence_repository.records", side_effect=SqlAdapterError("private SQL details", code=code)):
            response = client.get(f"/api/sessions/{sid}/evidence")
        body = response.json()
        assert response.status_code == 503
        assert body["error"]["code"] == code
        assert body["error"]["retryable"] is retryable
        assert body["error"]["preserve_evidence"] is True
        assert body["error"]["request_id"]
        assert "private SQL details" not in response.text
        assert "traceback" not in response.text.lower()


def test_oversized_business_key_is_rejected_without_repository_access():
    with TestClient(app) as client:
        sid = _unlocked_session(client)
        with patch("server.main.evidence_repository.records") as records:
            response = client.get(f"/api/sessions/{sid}/evidence", params={"business_key": "X" * 65})
        assert response.status_code == 422
        assert response.json()["error"]["code"] == "INVALID_REQUEST"
        records.assert_not_called()
