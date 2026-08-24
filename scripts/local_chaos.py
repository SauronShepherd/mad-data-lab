"""Failure-injection checks for recoverable Genie/session failures."""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
from server.main import app, genie


def main() -> None:
    with TestClient(app) as client:
        session = client.post("/api/sessions", json={"case_id": "CASE_0042"}).json()["session_id"]
        with patch.object(genie, "next", side_effect=TimeoutError("synthetic timeout")):
            response = client.post(f"/api/sessions/{session}/next", json={"completed_experiments": []})
            assert response.status_code == 200 and response.json()["source"] == "fixture"
        assert client.post("/api/sessions/missing/next", json={}).status_code == 404
        assert client.post(f"/api/sessions/{session}/chat", json={"question": "x" * 2001}).status_code == 422
        assert client.post("/api/sessions", json={"case_id": "CASE_../"}).status_code == 422
    print("local chaos: PASS (timeout fallback, missing session, oversized chat, invalid identifier)")


if __name__ == "__main__":
    main()
