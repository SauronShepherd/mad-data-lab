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
    print("local chaos: PASS (live timeout fails closed, missing session, oversized chat, invalid identifier)")


if __name__ == "__main__":
    main()
