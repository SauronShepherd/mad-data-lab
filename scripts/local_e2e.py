"""Deterministic API E2E for every Case in review mode.

This is the laptop substitute for the deployed browser suite: it exercises the
same public HTTP application contract with the fixture Genie path.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

os.environ["CHALLENGE_REVIEW_MODE"] = "1"

from fastapi.testclient import TestClient

from server.main import app
from server.catalog import FULL_CASE_CATALOG


def main() -> None:
    with TestClient(app) as client:
        for case in FULL_CASE_CATALOG:
            detail = client.get(f"/api/cases/{case.id}")
            assert detail.status_code == 200, (case.id, detail.text)
            if case.id != "CASE_0042":
                assert client.post("/api/sessions", json={"case_id": case.id}).status_code == 409
                continue
            session = client.post("/api/sessions", json={"case_id": case.id})
            assert session.status_code == 201, (case.id, session.text)
            session_id = session.json()["session_id"]
            experiments = client.get(f"/api/cases/{case.id}/experiments").json()["experiments"]
            completed: list[str] = []
            for _ in experiments:
                result = client.post(f"/api/sessions/{session_id}/next", json={})
                assert result.status_code == 200, (case.id, result.text)
                completed.append(result.json()["experiment_id"])
            verdict = client.post(f"/api/sessions/{session_id}/conclude")
            assert verdict.status_code == 200, (case.id, verdict.text)
            assert verdict.json()["status"] == "COMPLETE"
    print("local e2e: PASS (Case #042 journey; secondary Cases remain locked)")


if __name__ == "__main__":
    main()
