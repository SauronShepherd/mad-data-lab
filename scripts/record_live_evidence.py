"""Run authenticated live gates and bind their evidence to current source identity."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    "genie-eval.json": "scripts/live_genie_check.py",
    "deployed-smoke.json": "scripts/deployed_smoke.py",
    "deployed-soak.json": "scripts/deployed_soak.py",
}


def identity() -> dict:
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip() or "NOT_IN_GIT"
    runtime = subprocess.check_output([sys.executable, "scripts/compute_runtime_digest.py"], cwd=ROOT, text=True).strip()
    data = subprocess.check_output([sys.executable, "scripts/compute_mdl2_data_digest.py"], cwd=ROOT, text=True).strip()
    return {"git_head": head, "runtime_digest": runtime, "data_contract_digest": data}


def main() -> None:
    source_identity = identity()
    for filename, script in TARGETS.items():
        result = subprocess.run([sys.executable, script], cwd=ROOT, capture_output=True, text=True)
        payload = {
            "status": "PASS" if result.returncode == 0 else "FAIL",
            "command": [sys.executable, script],
            "output": (result.stdout + result.stderr)[-4000:],
            "source_identity": source_identity,
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        }
        (ROOT / "release-report" / filename).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"artifact": filename, "status": payload["status"]}))
        if result.returncode != 0:
            raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
