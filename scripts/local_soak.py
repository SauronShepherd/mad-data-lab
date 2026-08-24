"""Ten deterministic fixture investigations for the local release gate."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
from server.main import app


def main() -> None:
    with TestClient(app) as client:
        for run in range(10):
            created = client.post("/api/sessions", json={"case_id": "CASE_0042"})
            assert created.status_code == 201
            session_id = created.json()["session_id"]
            completed: list[str] = []
            for _ in range(3):
                response = client.post(f"/api/sessions/{session_id}/next", json={"completed_experiments": completed})
                assert response.status_code == 200, response.text
                completed.append(response.json()["experiment_id"])
            verdict = client.post(f"/api/sessions/{session_id}/conclude")
            assert verdict.status_code == 200
            assert verdict.json()["status"] == "COMPLETE"
    print("local soak: PASS (10 Case #042 investigations)")


if __name__ == "__main__":
    main()
