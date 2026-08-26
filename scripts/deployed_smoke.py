"""Authenticated deployed-app smoke gate."""
from __future__ import annotations

import os
import json
import subprocess
import time
from urllib.error import HTTPError, URLError
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

    def refresh_token() -> str:
        profile = os.getenv("DATABRICKS_CONFIG_PROFILE", "sda")
        return json.loads(subprocess.check_output(["databricks", "auth", "token", profile, "-o", "json"], text=True))["access_token"]

    def call(path: str, method: str = "GET", body: dict | None = None) -> dict:
        nonlocal token
        data = json.dumps(body).encode() if body is not None else None
        for attempt in range(3):
            request = Request(base + path, data=data, method=method, headers={"Accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {token}"})
            try:
                with urlopen(request, timeout=180) as response:
                    if response.status not in (200, 201):
                        raise SystemExit(f"deployed smoke: {path} HTTP {response.status}")
                    return json.loads(response.read().decode())
            except HTTPError as error:
                if error.code == 401 and attempt < 2 and not os.getenv("DATABRICKS_APP_TOKEN"):
                    token = refresh_token()
                elif error.code >= 500 and attempt < 2:
                    time.sleep(2 ** attempt)
                else:
                    # Preserve a small, sanitized response body so a failed
                    # deployment gate identifies the failing boundary (for
                    # example, an unavailable or invalid Genie response).
                    try:
                        detail = error.read(2048).decode("utf-8", errors="replace").replace("\n", " ")
                    except Exception:
                        detail = ""
                    raise RuntimeError(
                        f"deployed smoke: {path} HTTP {error.code}"
                        + (f"; detail={detail[:512]}" if detail else "")
                    ) from error
            except URLError:
                if attempt == 2:
                    raise
                time.sleep(2 ** attempt)
        raise RuntimeError("deployed smoke retry loop exhausted")

    assert call("/api/health")["status"] == "ok"
    cases = call("/api/cases")["cases"]
    assert any(item["id"] == "CASE_0042" for item in cases)
    session = call("/api/sessions", "POST", {"case_id": "CASE_0042"})
    session_id = session["session_id"]
    started = call(f"/api/sessions/{session_id}/start", "POST", {})
    assert started["state"] == "HYPOTHESES_READY"
    experiments = [call(f"/api/sessions/{session_id}/next", "POST", {}) for _ in range(5)]
    actual_experiment_ids = [item["experiment_id"] for item in experiments]
    expected_experiment_ids = [
        "COMPONENT_DECOMPOSITION", "SNAPSHOT_DIFF", "DQ_MATERIALITY", "FORMULA_VALIDATION", "RECONCILIATION"
    ]
    assert actual_experiment_ids == expected_experiment_ids, (
        f"unexpected deployed experiment sequence: {actual_experiment_ids}"
    )
    assert call(f"/api/sessions/{session_id}/evidence")["total"] >= 1
    assert call(f"/api/sessions/{session_id}/conclude", "POST", {})["status"] == "COMPLETE"
    print("deployed smoke: PASS (health, catalog, session, experiments, evidence, conclusion)")


if __name__ == "__main__":
    main()
