"""Five deterministic review-mode journeys for every secondary Case."""
from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ["CHALLENGE_REVIEW_MODE"] = "1"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from server.catalog import FULL_CASE_CATALOG
from server.main import PROGRESSION, SESSIONS, app


def main() -> None:
    secondary = [case.id for case in FULL_CASE_CATALOG if case.id != "CASE_0042"]
    with TestClient(app) as client:
        for case_id in secondary:
            for _ in range(5):
                SESSIONS.clear()
                PROGRESSION["completed_case_ids"].clear()
                created = client.post("/api/sessions", json={"case_id": case_id})
                assert created.status_code == 201, (case_id, created.text)
                session_id = created.json()["session_id"]
                experiments = client.get(f"/api/cases/{case_id}/experiments").json()["experiments"]
                for _ in experiments:
                    result = client.post(f"/api/sessions/{session_id}/next", json={})
                    assert result.status_code == 200, (case_id, result.text)
                verdict = client.post(f"/api/sessions/{session_id}/conclude")
                assert verdict.status_code == 200, (case_id, verdict.text)
    print(f"local secondary soak: PASS ({len(secondary)} Cases × 5 journeys)")


if __name__ == "__main__":
    main()
