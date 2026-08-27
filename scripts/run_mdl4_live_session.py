"""Run the canonical MDL-4 Case 042 path against a deployed App.

This gate is intentionally fail-closed: it never enables fixture mode and it
writes only sanitized session evidence (no access tokens or raw Genie text).
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "release-report" / "MDL-4" / "live-session.json"


def token() -> str:
    direct = os.getenv("DATABRICKS_APP_TOKEN")
    if direct:
        return direct
    profile = os.getenv("DATABRICKS_CONFIG_PROFILE", "mdl")
    payload = json.loads(subprocess.check_output(["databricks", "auth", "token", profile, "-o", "json"], text=True))
    return str(payload["access_token"])


def main() -> int:
    url = os.getenv("DEPLOYED_APP_URL")
    started = datetime.now(timezone.utc).isoformat()
    evidence = {"iteration": "MDL-4", "case_id": "CASE_0042", "status": "FAIL", "started_at": started}
    if not url:
        evidence.update(status="BLOCKED_EXTERNAL_CONFIGURATION", diagnostic="DEPLOYED_APP_URL is required")
        OUT.write_text(json.dumps(evidence, indent=2) + "\n")
        print(json.dumps(evidence, sort_keys=True))
        return 2
    base, auth = url.rstrip("/"), token()

    def call(path: str, method: str = "GET", body: dict | None = None) -> dict:
        data = json.dumps(body).encode() if body is not None else None
        req = Request(base + path, data=data, method=method, headers={"Accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {auth}"})
        with urlopen(req, timeout=180) as response:
            return json.loads(response.read().decode())

    try:
        health = call("/api/health")
        config = call("/api/config")
        cases = call("/api/cases")
        detail = call("/api/cases/CASE_0042")
        if health.get("genie_mode") != "live" or config.get("fixture_mode"):
            raise RuntimeError("deployed endpoint is not in live Genie mode")
        if not any(item.get("id") == "CASE_0042" for item in cases.get("cases", [])):
            raise RuntimeError("CASE_0042 is absent from deployed catalog")
        created = call("/api/sessions", "POST", {"case_id": "CASE_0042"})
        sid = str(created["session_id"])
        evidence["session_id_sha256"] = hashlib.sha256(sid.encode()).hexdigest()
        start = call(f"/api/sessions/{sid}/start", "POST", {})
        if start.get("state") != "HYPOTHESES_READY":
            raise RuntimeError(f"unexpected start state: {start.get('state')}")
        call(f"/api/sessions/{sid}/prediction", "POST", {"prediction": "PRED_SOURCE_VALUES_CHANGED"})
        experiments = []
        for _ in range(8):
            result = call(f"/api/sessions/{sid}/next", "POST", {"completed_experiments": experiments})
            if result.get("ready_for_final_prediction"):
                break
            experiment_id = result.get("experiment_id")
            if not experiment_id or experiment_id in experiments:
                raise RuntimeError("invalid or repeated experiment selection")
            experiments.append(experiment_id)
        if len(experiments) != 5:
            raise RuntimeError(f"expected 5 experiments, got {experiments}")
        call(f"/api/sessions/{sid}/evidence/inspect", "POST", {"capability": "CASE_0042:RECORD:TX-004291"})
        call(f"/api/sessions/{sid}/evidence/inspect", "POST", {"capability": "CASE_0042:LINEAGE:V2_SOURCE_PATH"})
        call(f"/api/sessions/{sid}/evidence/inspect", "POST", {"capability": "CASE_0042:DQ:MATERIALITY"})
        call(f"/api/sessions/{sid}/prediction", "POST", {"prediction": "FINAL_CHANGED_V2_SOURCE_RECORDS", "final": True})
        conclusion = call(f"/api/sessions/{sid}/conclude", "POST", {})
        debrief = call(f"/api/sessions/{sid}/debrief", "POST", {})
        if debrief.get("score") != 1000:
            raise RuntimeError(f"expected score 1000, got {debrief.get('score')}")
        evidence.update(status="PASS", health=health.get("status"), case_title=detail.get("case", {}).get("title"), experiments=experiments, score=debrief.get("score"), state=debrief.get("state"), conclusion_status=conclusion.get("state"), finished_at=datetime.now(timezone.utc).isoformat())
    except Exception as exc:
        evidence.update(status="LIVE_GENIE_PROTOCOL_FAILURE", diagnostic=str(exc)[:512], finished_at=datetime.now(timezone.utc).isoformat())
    OUT.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    print(json.dumps(evidence, sort_keys=True))
    return 0 if evidence["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
