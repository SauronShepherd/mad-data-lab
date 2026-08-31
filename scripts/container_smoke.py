"""Smoke the locally packaged Docker service without external credentials."""
from __future__ import annotations

import json
import os
import time
from urllib.error import URLError
from urllib.request import Request, urlopen


BASE = os.getenv("CONTAINER_BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def call(path: str, method: str = "GET", body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    request = Request(BASE + path, data=data, method=method, headers={"Accept": "application/json", "Content-Type": "application/json"})
    with urlopen(request, timeout=30) as response:
        if response.status not in (200, 201):
            raise AssertionError(f"{path}: HTTP {response.status}")
        return json.loads(response.read().decode())


def main() -> None:
    # `docker compose up -d` only starts the process; it does not wait for
    # Uvicorn's socket to accept requests.  Bound the readiness wait so a
    # crashed container still fails quickly and diagnostically in CI.
    last_error: Exception | None = None
    for _ in range(90):
        try:
            if call("/health")["status"] == "ok":
                break
        except (URLError, ConnectionError, TimeoutError, OSError) as exc:
            last_error = exc
        time.sleep(1)
    else:
        raise AssertionError(f"container did not become ready: {last_error}")
    session = call("/api/sessions", "POST", {"case_id": "CASE_0042"})
    assert session["state"] == "CASE_BRIEFING"
    assert session.get("score_visibility") == "HIDDEN_DURING_INVESTIGATION"
    session_id = session["session_id"]
    started = call(f"/api/sessions/{session_id}/start", "POST", {})
    assert started["state"] == "HYPOTHESES_READY"
    call(f"/api/sessions/{session_id}/prediction", "POST", {"prediction": "PRED_SOURCE_VALUES_CHANGED"})
    results = [call(f"/api/sessions/{session_id}/next", "POST", {}) for _ in range(5)]
    assert [item["experiment_id"] for item in results] == [
        "COMPONENT_DECOMPOSITION", "SNAPSHOT_DIFF", "DQ_MATERIALITY", "FORMULA_VALIDATION", "RECONCILIATION"
    ]
    assert call(f"/api/sessions/{session_id}/evidence")["total"] == 30
    call(f"/api/sessions/{session_id}/evidence/inspect", "POST", {"capability": "CASE_0042:LINEAGE:V2_SOURCE_PATH"})
    final_stage = call(f"/api/sessions/{session_id}/next", "POST", {})
    assert final_stage["phase"] == "PLAYER_PREDICTION_FINAL"
    call(f"/api/sessions/{session_id}/prediction", "POST", {"final": True, "prediction": "FINAL_CHANGED_V2_SOURCE_RECORDS"})
    assert call(f"/api/sessions/{session_id}/conclude", "POST", {})["state"] == "CONCLUDING"
    assert call(f"/api/sessions/{session_id}/debrief", "POST", {})["state"] == "DEBRIEF"
    print("container smoke: PASS (canonical MDL-4 Case #042 session)")


if __name__ == "__main__":
    main()
