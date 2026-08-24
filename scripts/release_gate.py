"""Run local release gates and write the specification's release report."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "release-report"

GATES = {
    "lint": [sys.executable, "-m", "compileall", "-q", "server", "tests", "scripts"],
    "typecheck": [sys.executable, "-m", "mypy", "server", "--ignore-missing-imports", "--follow-imports=skip", "--no-site-packages"],
    "unit": [sys.executable, "-m", "pytest", "-q"],
    "data": [sys.executable, "-m", "pytest", "-q", "tests/test_domain.py", "tests/test_mutation.py"],
    "contract": [sys.executable, "-m", "pytest", "-q", "tests/test_case_contract.py"],
    "e2e": [sys.executable, "scripts/local_e2e.py"],
    "visual": [sys.executable, "scripts/visual_gate.py"],
    "assets": [sys.executable, "scripts/assets_gate.py"],
    "security": [sys.executable, "scripts/security_gate.py"],
    "a11y": [sys.executable, "scripts/a11y_gate.py"],
    "chaos": [sys.executable, "scripts/local_chaos.py"],
    "soak": [sys.executable, "scripts/local_soak.py"],
}


def run(name: str, command: list[str]) -> dict:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    return {"name": name, "command": command, "status": "PASS" if result.returncode == 0 else "FAIL", "output": (result.stdout + result.stderr)[-4000:]}


def main() -> None:
    REPORT.mkdir(exist_ok=True)
    results = [run(name, command) for name, command in GATES.items()]
    failed = [item["name"] for item in results if item["status"] != "PASS"]
    (REPORT / "test-results.xml").write_text(
        "<testsuite name=\"mad-data-lab-local\" tests=\"%d\" failures=\"%d\"/>\n" % (len(results), len(failed)),
        encoding="utf-8",
    )
    (REPORT / "golden-case.json").write_text(json.dumps({"status": "PASS" if not failed else "FAIL", "gates": results}, indent=2), encoding="utf-8")
    live_payloads = {
        "genie-eval.json": {"status": "NOT_RUN", "reason": "requires authenticated live Genie"},
        "deployed-smoke.json": {"status": "NOT_RUN", "reason": "requires authenticated deployed app"},
        "deployed-soak.json": {"status": "NOT_RUN", "reason": "requires authenticated deployed app"},
    }
    if os.getenv("RUN_LIVE_GATES") != "1":
        for name in live_payloads:
            existing_path = REPORT / name
            if existing_path.exists():
                try:
                    existing = json.loads(existing_path.read_text(encoding="utf-8"))
                    if existing.get("status") == "PASS":
                        live_payloads[name] = existing
                except (OSError, json.JSONDecodeError):
                    pass
    if os.getenv("RUN_LIVE_GATES") == "1":
        live_commands = {
            "genie-eval.json": [sys.executable, "scripts/live_genie_check.py"],
            "deployed-smoke.json": [sys.executable, "scripts/deployed_smoke.py"],
            "deployed-soak.json": [sys.executable, "scripts/deployed_soak.py"],
        }
        for name, command in live_commands.items():
            live_payloads[name] = run(name, command)
    for name, payload in (("genie-eval.json", live_payloads["genie-eval.json"]), ("asset-preflight.json", next(item for item in results if item["name"] == "assets")), ("visual-diff-summary.json", next(item for item in results if item["name"] == "visual")), ("deployed-smoke.json", live_payloads["deployed-smoke.json"]), ("deployed-soak.json", live_payloads["deployed-soak.json"])):
        (REPORT / name).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    summary = ["# MAD DATA LAB release report", "", f"Generated: {datetime.now(timezone.utc).isoformat()}", "", f"Local gates: {'PASS' if not failed else 'FAIL'}"]
    summary += [f"- {item['name']}: {item['status']}" for item in results]
    live_status = "PASS" if all(payload.get("status") == "PASS" for payload in live_payloads.values()) else "NOT RUN"
    summary += ["", f"Live Genie/deployed gates: {live_status}."]
    (REPORT / "summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    if failed:
        raise SystemExit(f"release gate failed: {', '.join(failed)}")
    print(f"release gate: PASS ({len(results)} local gates; live gates: {live_status})")


if __name__ == "__main__":
    main()
