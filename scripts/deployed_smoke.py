"""Authenticated deployed-app smoke gate."""
from __future__ import annotations

import os
import json
import subprocess
from urllib.request import Request, urlopen


def main() -> None:
    url = os.getenv("DEPLOYED_APP_URL")
    if not url:
        raise SystemExit("deployed smoke: NOT RUN; set DEPLOYED_APP_URL")
    token = os.getenv("DATABRICKS_APP_TOKEN")
    if not token:
        profile = os.getenv("DATABRICKS_CONFIG_PROFILE", "sda")
        token = json.loads(subprocess.check_output(["databricks", "auth", "token", profile, "-o", "json"], text=True))["access_token"]
    base = url.rstrip("/")

    def call(path: str, method: str = "GET", body: dict | None = None) -> dict:
        data = json.dumps(body).encode() if body is not None else None
        request = Request(base + path, data=data, method=method, headers={"Accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {token}"})
        with urlopen(request, timeout=180) as response:
            if response.status != 200 and response.status != 201:
                raise SystemExit(f"deployed smoke: {path} HTTP {response.status}")
            return json.loads(response.read().decode())

    assert call("/api/health")["status"] == "ok"
    cases = call("/api/cases")["cases"]
    assert any(item["id"] == "CASE_0042" for item in cases)
    session = call("/api/sessions", "POST", {"case_id": "CASE_0042"})
    session_id = session["session_id"]
    for _ in range(3):
        call(f"/api/sessions/{session_id}/next", "POST", {})
    assert call(f"/api/sessions/{session_id}/evidence")["total"] >= 1
    assert call(f"/api/sessions/{session_id}/conclude", "POST", {})["status"] == "COMPLETE"
    print("deployed smoke: PASS (health, catalog, session, experiments, evidence, conclusion)")


if __name__ == "__main__":
    main()
