import asyncio
import re
from pathlib import Path
from fastapi.testclient import TestClient
from starlette.requests import Request

from server.errors import AppError, ERROR_CODES, app_error_from_exception, envelope
from backend.data.sql_client import SqlAdapterError
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


def test_all_literal_api_error_codes_are_registered():
    source = (Path(__file__).parents[1] / "server/main.py").read_text(encoding="utf-8")
    emitted = set(re.findall(r'code["\']?\s*[:=]\s*["\']([A-Z][A-Z0-9_]+)', source))
    assert emitted <= ERROR_CODES, sorted(emitted - ERROR_CODES)


def test_app_error_rejects_unregistered_codes():
    import pytest
    with pytest.raises(ValueError, match="unregistered application error code"):
        AppError("NOT_REGISTERED", "should never be emitted")


def test_unhandled_request_failure_is_safe():
    async def fail(_request):
        raise RuntimeError("secret backend traceback")
    scope = {"type": "http", "method": "GET", "path": "/boom", "headers": [], "query_string": b"", "scheme": "http", "server": ("test", 80), "client": ("test", 1), "root_path": ""}
    response = asyncio.run(__import__("server.main", fromlist=["request_id_middleware"]).request_id_middleware(Request(scope), fail))
    assert response.status_code == 503
    assert response.body.find(b"APP_RESOURCE_UNAVAILABLE") >= 0
    assert b"secret backend traceback" not in response.body


def test_adapter_errors_convert_to_safe_public_platform_envelopes():
    error = app_error_from_exception(SqlAdapterError("private provider detail", code="WAREHOUSE_PENDING"))
    body = envelope(error, "req-platform")
    assert body["error"]["code"] == "WAREHOUSE_PENDING"
    assert body["error"]["retryable"] is True
    assert body["error"]["preserve_evidence"] is True
    assert "private provider" not in str(body)
