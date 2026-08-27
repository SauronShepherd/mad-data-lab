from fastapi.testclient import TestClient

from server.errors import AppError, envelope
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
