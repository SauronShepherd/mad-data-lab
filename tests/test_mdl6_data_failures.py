from unittest.mock import patch

from fastapi.testclient import TestClient

from server.main import SESSIONS, app


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
