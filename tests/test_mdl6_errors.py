from fastapi.testclient import TestClient

from server.errors import AppError, ERROR_CODES, envelope
from server.main import app


def test_error_envelope_is_stable_and_safe():
    body = envelope(AppError("GENIE_TIMEOUT", "private detail", 504, True), "req-1")
    assert body == {"error": {"code": "GENIE_TIMEOUT", "message": "private detail", "retryable": True, "preserve_evidence": True, "request_id": "req-1"}}


def test_unknown_session_uses_stable_error_envelope_and_request_id():
    response = TestClient(app).get("/api/sessions/missing")
    assert response.status_code == 404
    assert response.headers["X-Request-ID"]
    assert response.json()["error"]["code"] == "SESSION_NOT_FOUND"
    assert "traceback" not in response.text.lower()


def test_validation_errors_use_stable_error_envelope():
    response = TestClient(app).post("/api/sessions", json={"case_id": "not-a-case"})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_REQUEST"
    assert response.headers["X-Request-ID"] == response.json()["error"]["request_id"]


def test_mdl6_error_taxonomy_contains_required_categories():
    required = {"GENIE_TIMEOUT", "GENIE_FAILED", "GENIE_MALFORMED_PROTOCOL", "CASE_NOT_FOUND", "EVIDENCE_SCHEMA_MISMATCH", "RECONCILIATION_FAILED", "DATA_INVARIANT_FAILED", "ILLEGAL_STATE_TRANSITION", "SESSION_NOT_FOUND", "DUPLICATE_ACTION", "WAREHOUSE_PENDING", "WAREHOUSE_QUOTA_EXHAUSTED", "APP_RESOURCE_UNAVAILABLE"}
    assert required <= ERROR_CODES
