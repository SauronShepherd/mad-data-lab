"""Run local release gates and write the specification's release report."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "release-report"
NPM = "npm.cmd" if os.name == "nt" else "npm"
GATE_TIMEOUT_SECONDS = int(os.getenv("MDL3_GATE_TIMEOUT_SECONDS", "300"))

def source_identity() -> dict[str, Any]:
    """Bind local evidence to the source tree that produced it."""
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    dirty = bool(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True).stdout.strip())
    runtime = subprocess.run([sys.executable, "scripts/compute_runtime_digest.py"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    data = subprocess.run([sys.executable, "scripts/compute_mdl2_data_digest.py"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return {"git_head": head or "NOT_IN_GIT", "git_worktree_dirty": dirty, "runtime_digest": runtime, "data_contract_digest": data}

GATES = {
    "lint": [sys.executable, "-m", "compileall", "-q", "server", "tests", "scripts"],
    "typecheck": [NPM, "run", "typecheck"],
    "unit": [sys.executable, "scripts/pytest_gate.py", "--junitxml=release-report/pytest-results.xml", "-q"],
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
    "art_preflight": [sys.executable, "scripts/build_mdl3_art_review.py"],
    "mdl1_art_preflight": [sys.executable, "scripts/build_mdl1_art_review.py"],
    "browser": [NPM, "run", "test:browser"],
    "mdl2_contract": [sys.executable, "scripts/validate_mdl2_contract.py"],
    "mdl3_contract": [sys.executable, "scripts/validate_mdl3_contract.py", "--strict"],
    "mdl3_benchmark": [sys.executable, "scripts/run_mdl3_benchmark.py"],
    "live_sql_plan": [sys.executable, "scripts/live_sql_check.py", "--plan"],
    "traceability": [sys.executable, "scripts/validate_traceability.py"],
    "a11y": [sys.executable, "scripts/a11y_gate.py"],
    "chaos": [sys.executable, "scripts/local_chaos.py"],
    "soak": [sys.executable, "scripts/local_soak.py"],
}


def run(name: str, command: list[str]) -> dict:
    try:
        result = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=GATE_TIMEOUT_SECONDS,
        )
        return {
            "name": name,
            "command": command,
            "status": "PASS" if result.returncode == 0 else "FAIL",
            "output": (result.stdout + result.stderr)[-4000:],
        }
    except subprocess.TimeoutExpired as exc:
        output = "".join(
            part.decode(errors="replace") if isinstance(part, bytes) else (part or "")
            for part in (exc.stdout, exc.stderr)
        )
        return {
            "name": name,
            "command": command,
            "status": "FAIL",
            "output": f"timed out after {GATE_TIMEOUT_SECONDS}s\n{output}"[-4000:],
        }


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
    live_payloads: dict[str, dict[str, Any]] = {
        "genie-eval.json": {"status": "NOT_RUN", "reason": "requires authenticated live Genie"},
        "deployed-smoke.json": {"status": "NOT_RUN", "reason": "requires authenticated deployed app"},
        "deployed-soak.json": {"status": "NOT_RUN", "reason": "requires authenticated deployed app"},
    }
    # Preserve recorded failures for auditability, but never reuse a PASS:
    # live evidence is valid only for the invocation that produced it.
    for name in live_payloads:
        prior = REPORT / name
        if prior.exists():
            try:
                candidate = json.loads(prior.read_text(encoding="utf-8"))
                if isinstance(candidate, dict) and candidate.get("status") == "FAIL":
                    live_payloads[name] = candidate
            except (OSError, json.JSONDecodeError):
                pass
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
    live_values = [payload.get("status") for payload in live_payloads.values()]
    live_status = (
        "PASS" if all(value == "PASS" for value in live_values)
        else "FAIL" if any(value == "FAIL" for value in live_values)
        else "NOT RUN"
    )
    summary += ["", f"Live Genie/deployed gates: {live_status}."]
    (REPORT / "summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    # MDL-7 requires a self-contained release bundle. Keep each artifact
    # truthful: live evidence is produced only when RUN_LIVE_GATES=1.
    mdl7 = REPORT / "MDL-7"
    mdl7.mkdir(parents=True, exist_ok=True)
    local_by_name = {item["name"]: item for item in results}
    artifact_map = {
        "genie-eval.json": live_payloads["genie-eval.json"],
        "deployed-smoke.json": live_payloads["deployed-smoke.json"],
        "live-soak.json": live_payloads["deployed-soak.json"],
        "golden-case.json": {"status": "PASS" if not failed else "FAIL", "source_identity": identity},
        "asset-preflight.json": local_by_name.get("assets", {"status": "NOT_RUN"}),
        "accessibility-summary.json": local_by_name.get("a11y", {"status": "NOT_RUN"}),
        "security-summary.json": local_by_name.get("security", {"status": "NOT_RUN"}),
        "performance-summary.json": local_by_name.get("performance", {"status": "NOT_RUN"}),
        "visual-diff-summary.json": local_by_name.get("visual", {"status": "NOT_RUN"}),
    }
    for filename, payload in artifact_map.items():
        (mdl7 / filename).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    audio_result = run("audio-preflight", [sys.executable, "scripts/audio_preflight.py"])
    (mdl7 / "audio-preflight.json").write_text(json.dumps(audio_result, indent=2) + "\n", encoding="utf-8")
    (mdl7 / "test-results.xml").write_bytes((REPORT / "test-results.xml").read_bytes())
    gate_lines = ["# MDL-7 release report", "", f"Source: `{identity['git_head']}`", "", "## Gates", ""]
    gate_lines.extend(f"- {item['name']}: {item['status']}" for item in results)
    gate_lines.extend([
        f"- live-genie: {live_payloads['genie-eval.json'].get('status', 'NOT_RUN')}",
        f"- deployed-smoke: {live_payloads['deployed-smoke.json'].get('status', 'NOT_RUN')}",
        f"- deployed-soak: {live_payloads['deployed-soak.json'].get('status', 'NOT_RUN')}",
        "",
        "Live PASS requires authenticated execution for the current source identity; no stale PASS is reused.",
    ])
    (mdl7 / "summary.md").write_text("\n".join(gate_lines) + "\n", encoding="utf-8")
    if failed:
        raise SystemExit(f"release gate failed: {', '.join(failed)}")
    print(f"release gate: PASS ({len(results)} local gates; live gates: {live_status})")


if __name__ == "__main__":
    main()
