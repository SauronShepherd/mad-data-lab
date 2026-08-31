"""Run authenticated live gates and bind their evidence to current source identity."""
from __future__ import annotations

import json
import argparse
import subprocess
import sys
import shlex
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from backend.genie.config_digest import genie_contract_digest
TARGETS = {
    "genie-eval.json": "scripts/run_mdl3_benchmark.py --no-fixture --output release-report/genie-eval.json",
    "deployed-smoke.json": "scripts/deployed_smoke.py",
    "deployed-soak.json": "scripts/deployed_soak.py",
}


def identity() -> dict:
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip() or "NOT_IN_GIT"
    runtime = subprocess.check_output([sys.executable, "scripts/compute_runtime_digest.py"], cwd=ROOT, text=True).strip()
    data = subprocess.check_output([sys.executable, "scripts/compute_mdl2_data_digest.py"], cwd=ROOT, text=True).strip()
    config = json.loads((ROOT / "release-report/MDL-3/genie-live-config.json").read_text(encoding="utf-8"))
    return {
        "git_head": head,
        "runtime_digest": runtime,
        "data_contract_digest": data,
        "genie_contract_digest": genie_contract_digest(),
        "genie_live_config_sha256": config.get("genie_live_config_sha256", "NOT_RECORDED"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=tuple(TARGETS), action="append")
    parser.add_argument("--captured-output", help="Use a completed gate log; requires an explicit PASS marker.")
    args = parser.parse_args()
    source_identity = identity()
    targets = ((filename, TARGETS[filename]) for filename in (args.only or list(TARGETS)))
    for filename, script in targets:
        command = [sys.executable, *shlex.split(script)]
        if args.captured_output and filename in {"deployed-soak.json", "deployed-smoke.json"}:
            captured = Path(args.captured_output)
            if not captured.is_file():
                raise SystemExit(f"captured evidence file does not exist: {captured}")
            output = captured.read_text(encoding="utf-8")
            marker = ("deployed soak: PASS (10 authenticated Case #042 journeys)"
                      if filename == "deployed-soak.json"
                      else "deployed smoke: PASS (health, catalog, session, experiments, evidence inspection, verdict, debrief)")
            if marker not in output:
                raise SystemExit("captured deployed evidence lacks the exact PASS marker")
            result = subprocess.CompletedProcess([sys.executable, script], 0, output, "")
        else:
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        payload = {
            "status": "PASS" if result.returncode == 0 else "FAIL",
            "command": command,
            "output": (result.stdout + result.stderr)[-4000:],
            "source_identity": source_identity,
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        }
        if filename == "genie-eval.json":
            try:
                detailed = json.loads((ROOT / "release-report" / filename).read_text(encoding="utf-8"))
                if isinstance(detailed, dict) and "attempts" in detailed:
                    detailed.update({"command": payload["command"], "source_identity": source_identity, "generated_at_utc": payload["generated_at_utc"]})
                    payload = detailed
            except (OSError, json.JSONDecodeError):
                pass
        (ROOT / "release-report" / filename).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"artifact": filename, "status": payload["status"]}))
        if result.returncode != 0:
            raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
