"""Failure-injection checks for recoverable Genie/session failures."""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
from fastapi import HTTPException
from server.main import app


def main() -> None:
    with TestClient(app) as client:
        session = client.post("/api/sessions", json={"case_id": "CASE_0042"}).json()["session_id"]
        assert client.post(f"/api/sessions/{session}/start").status_code == 200
        duplicate_start = client.post(f"/api/sessions/{session}/start")
        assert duplicate_start.status_code == 409
        idem_headers = {"Idempotency-Key": "chaos-create-1"}
        first_create = client.post("/api/sessions", json={"case_id": "CASE_0042"}, headers=idem_headers)
        replay_create = client.post("/api/sessions", json={"case_id": "CASE_0042"}, headers=idem_headers)
        assert first_create.status_code == replay_create.status_code == 201
        assert first_create.json()["session_id"] == replay_create.json()["session_id"]
        failed_genie = SimpleNamespace(enabled=True, next=lambda *_args, **_kwargs: (_ for _ in ()).throw(TimeoutError("synthetic timeout")))
        with patch("server.main.genie", failed_genie), patch("server.main.next_experiment", side_effect=HTTPException(status_code=503, detail="unavailable")):
            response = client.post(f"/api/sessions/{session}/next", json={"completed_experiments": []})
            assert response.status_code == 503, response.text
            assert response.json()["error"]["code"] == "GENIE_EXPERIMENT_UNAVAILABLE"
            assert response.json()["error"]["retryable"] is True
            assert response.json()["detail"]["code"] == "GENIE_EXPERIMENT_UNAVAILABLE"
            assert client.get(f"/api/sessions/{session}").json()["completed"] == []
        assert client.post("/api/sessions/missing/next", json={}).status_code == 404
        assert client.post(f"/api/sessions/{session}/chat", json={"question": "x" * 2001}).status_code == 422
        assert client.post("/api/sessions", json={"case_id": "CASE_../"}).status_code == 422
        malformed = client.post(
            "/api/sessions",
            content=b"{",
            headers={"Content-Type": "application/json"},
        )
        assert malformed.status_code == 422
        assert malformed.json()["error"]["code"] == "INVALID_REQUEST"
        unsupported_case = client.post(
            "/api/experiments/next",
            json={"case_id": "CASE_9999", "completed_experiments": []},
        )
        assert unsupported_case.status_code == 404
        missing_query = client.post("/api/genie/ask", json={"case_id": "CASE_0042"})
        assert missing_query.status_code == 422
        assert missing_query.json()["error"]["code"] == "INVALID_REQUEST"
        unicode_chat = client.post(
            f"/api/sessions/{session}/chat",
            json={"question": "¿Qué cambió en V2? Δ业务🔬"},
        )
        assert unicode_chat.status_code == 200
        for _ in range(9):
            assert client.post(f"/api/sessions/{session}/chat", json={"question": "retry"}).status_code == 200
        rate_limited = client.post(f"/api/sessions/{session}/chat", json={"question": "one-too-many"})
        assert rate_limited.status_code == 429
    print("local chaos: PASS (fails closed on timeout, missing session, oversized chat, invalid identifier, malformed JSON, unsupported Case, missing query, duplicate actions, Unicode input, rate limit)")


if __name__ == "__main__":
    main()
