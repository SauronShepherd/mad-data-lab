from fastapi import HTTPException
from fastapi.testclient import TestClient

from server.main import app


def test_missing_case_route_uses_case_error_code():
    response = TestClient(app).get("/api/cases/CASE_9999")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "CASE_NOT_FOUND"


def test_unearned_evidence_uses_stable_data_error_code():
    client = TestClient(app)
    session = client.post("/api/sessions", json={"case_id": "CASE_0042"}).json()["session_id"]
    response = client.get(f"/api/sessions/{session}/evidence")
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "EVIDENCE_SCHEMA_MISMATCH"
