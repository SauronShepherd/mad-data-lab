"""Validate deterministic secondary-Case catalog visibility and lock state."""
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
        catalog = {item["id"]: item for item in client.get("/api/cases").json()["cases"]}
        for case_id in secondary:
            assert catalog[case_id]["availability"] == "LOCKED", (case_id, catalog[case_id])
            created = client.post("/api/sessions", json={"case_id": case_id})
            assert created.status_code == 409, (case_id, created.text)
    print(f"local secondary catalog gate: PASS ({len(secondary)} Cases remain locked)")


if __name__ == "__main__":
    main()
