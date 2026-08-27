"""Deterministic fake-Genie Case #042 path from board to Debrief."""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from server.main import app, PROGRESSION, SESSIONS

def main():
    SESSIONS.clear(); PROGRESSION["completed_case_ids"].clear(); PROGRESSION["best_scores"].clear()
    client = TestClient(app)
    created = client.post("/api/sessions", json={"case_id":"CASE_0042"}); assert created.status_code == 201
    sid = created.json()["session_id"]
    assert client.post(f"/api/sessions/{sid}/start").status_code == 200
    assert client.post(f"/api/sessions/{sid}/prediction", json={"prediction":"PRED_SOURCE_VALUES_CHANGED"}).status_code == 200
    experiments = []
    for _ in range(5):
        response = client.post(f"/api/sessions/{sid}/next", json={}); assert response.status_code == 200
        experiments.append(response.json()["experiment_id"])
    assert client.post(f"/api/sessions/{sid}/next", json={}).json()["phase"] == "PLAYER_PREDICTION_FINAL"
    assert client.post(f"/api/sessions/{sid}/evidence/inspect", json={"capability":"CASE_0042:RECORD:TX-004291"}).status_code == 200
    assert client.post(f"/api/sessions/{sid}/evidence/inspect", json={"capability":"CASE_0042:LINEAGE:V2_SOURCE_PATH"}).status_code == 200
    assert client.post(f"/api/sessions/{sid}/prediction", json={"final":True,"prediction":"FINAL_CHANGED_V2_SOURCE_RECORDS"}).status_code == 200
    verdict = client.post(f"/api/sessions/{sid}/conclude", json={}); assert verdict.status_code == 200
    debrief = client.post(f"/api/sessions/{sid}/debrief", json={}); assert debrief.status_code == 200
    assert debrief.json()["score"] == 1000
    result = {"status":"PASS", "session_id":sid, "experiments":experiments, "state":debrief.json()["state"], "score":debrief.json()["score"]}
    print(json.dumps(result, indent=2))

if __name__ == "__main__": main()
