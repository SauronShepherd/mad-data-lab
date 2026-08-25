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
NPM = "npm.cmd" if os.name == "nt" else "npm"

def source_identity() -> dict:
    """Bind local evidence to the source tree that produced it."""
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    dirty = bool(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True).stdout.strip())
    runtime = subprocess.run([sys.executable, "scripts/compute_runtime_digest.py"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    data = subprocess.run([sys.executable, "scripts/compute_mdl2_data_digest.py"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return {"git_head": head or "NOT_IN_GIT", "git_worktree_dirty": dirty, "runtime_digest": runtime, "data_contract_digest": data}

GATES = {
    "lint": [sys.executable, "-m", "compileall", "-q", "server", "tests", "scripts"],
    "typecheck": [sys.executable, "-m", "mypy", "server", "--ignore-missing-imports", "--follow-imports=skip", "--no-site-packages"],
    "unit": [sys.executable, "-m", "pytest", "-q", "--junitxml=release-report/pytest-results.xml"],
    "data": [sys.executable, "-m", "pytest", "-q", "tests/test_domain.py", "tests/test_mutation.py"],
    "mdl2_property": [sys.executable, "scripts/mdl2_property_suite.py"],
    "mdl2_data_deploy_local": [sys.executable, "scripts/verify_databricks_data.py", "--target", "local"],
    "mdl2_sql_preflight": [sys.executable, "scripts/mdl2_sql_preflight.py"],
    "contract": [sys.executable, "-m", "pytest", "-q", "tests/test_case_contract.py"],
    "e2e": [sys.executable, "scripts/local_e2e.py"],
    "visual": [sys.executable, "scripts/visual_gate.py"],
    "assets": [sys.executable, "scripts/assets_gate.py"],
    "security": [sys.executable, "scripts/security_gate.py"],
    "frontend_contract": [sys.executable, "scripts/frontend_contract_gate.py"],
    "art_contact_sheets": [sys.executable, "scripts/build_art_contact_sheets.py"],
    "art_preflight": [sys.executable, "scripts/build_mdl2_art_review.py"],
    "mdl1_art_preflight": [sys.executable, "scripts/build_mdl1_art_review.py"],
    "browser": [NPM, "run", "test:browser"],
    "mdl2_contract": [sys.executable, "scripts/validate_mdl2_contract.py"],
    "live_sql_plan": [sys.executable, "scripts/live_sql_check.py", "--plan"],
    "traceability": [sys.executable, "scripts/validate_traceability.py"],
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
    pytest_report = REPORT / "pytest-results.xml"
    if pytest_report.exists():
        (REPORT / "test-results.xml").write_bytes(pytest_report.read_bytes())
    else:
        (REPORT / "test-results.xml").write_text(
            "<testsuite name=\"mad-data-lab-local\" tests=\"%d\" failures=\"%d\"/>\n" % (len(results), len(failed)),
            encoding="utf-8",
        )
    (REPORT / "golden-case.json").write_text(json.dumps({"status": "PASS" if not failed else "FAIL", "source_identity": source_identity(), "gates": results}, indent=2), encoding="utf-8")
    live_payloads = {
        "genie-eval.json": {"status": "NOT_RUN", "reason": "requires authenticated live Genie"},
        "deployed-smoke.json": {"status": "NOT_RUN", "reason": "requires authenticated deployed app"},
        "deployed-soak.json": {"status": "NOT_RUN", "reason": "requires authenticated deployed app"},
    }
    # Never reuse a previous PASS: evidence is valid only for the invocation
    # that produced it and must be explicitly rerun for live/deployed checks.
    if os.getenv("RUN_LIVE_GATES") == "1":
        live_identity = source_identity()
        live_commands = {
            "genie-eval.json": [sys.executable, "scripts/live_genie_check.py"],
            "deployed-smoke.json": [sys.executable, "scripts/deployed_smoke.py"],
            "deployed-soak.json": [sys.executable, "scripts/deployed_soak.py"],
        }
        for name, command in live_commands.items():
            live_payloads[name] = run(name, command)
            live_payloads[name]["source_identity"] = live_identity
            live_payloads[name]["generated_at_utc"] = datetime.now(timezone.utc).isoformat()
    for name, payload in (("genie-eval.json", live_payloads["genie-eval.json"]), ("asset-preflight.json", next(item for item in results if item["name"] == "assets")), ("visual-diff-summary.json", next(item for item in results if item["name"] == "visual")), ("deployed-smoke.json", live_payloads["deployed-smoke.json"]), ("deployed-soak.json", live_payloads["deployed-soak.json"])):
        (REPORT / name).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    identity = source_identity()
    summary = ["# MAD DATA LAB release report", "", f"Generated: {datetime.now(timezone.utc).isoformat()}", f"Source identity: git_head={identity['git_head']} dirty={identity['git_worktree_dirty']}", f"Runtime digest: {identity['runtime_digest']}", f"Data contract digest: {identity['data_contract_digest']}", "", f"Local gates: {'PASS' if not failed else 'FAIL'}"]
    summary += [f"- {item['name']}: {item['status']}" for item in results]
    live_status = "PASS" if all(payload.get("status") == "PASS" for payload in live_payloads.values()) else "NOT RUN"
    summary += ["", f"Live Genie/deployed gates: {live_status}."]
    (REPORT / "summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    if failed:
        raise SystemExit(f"release gate failed: {', '.join(failed)}")
    print(f"release gate: PASS ({len(results)} local gates; live gates: {live_status})")


if __name__ == "__main__":
    main()
