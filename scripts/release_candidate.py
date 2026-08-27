"""Authoritative fail-closed MDL-5 release-candidate orchestration."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import shutil
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts import release_gate

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "release-report/MDL-5/release-candidate.json"

# Ordered deliberately: source checks, contracts, tests, UI, then soak/live.
ORDER = tuple(release_gate.GATES)


def identity() -> dict[str, str]:
    def git(*args: str) -> str:
        result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    return {
        "branch": git("branch", "--show-current"),
        "commit_sha": git("rev-parse", "HEAD"),
        "tree_sha": git("rev-parse", "HEAD^{tree}"),
        "runtime_digest": subprocess.check_output([sys.executable, "scripts/compute_runtime_digest.py"], cwd=ROOT, text=True).strip(),
        "data_contract_digest": subprocess.check_output([sys.executable, "scripts/compute_mdl2_data_digest.py"], cwd=ROOT, text=True).strip(),
    }


def asset_hashes() -> dict[str, str]:
    result = {}
    for path in sorted((ROOT / "public/assets").rglob("*")):
        if path.is_file():
            result[str(path.relative_to(ROOT)).replace("\\", "/")] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def test_counts() -> dict[str, int]:
    path = ROOT / "release-report/MDL-5/pytest-gate.xml"
    if not path.is_file():
        return {"collected": 0, "passed": 0, "skipped": 0, "failed": 0}
    import xml.etree.ElementTree as ET
    root = ET.parse(path).getroot()
    suite = root.find("testsuite")
    if suite is None:
        suite = root
    return {key: int(suite.attrib.get(key, 0)) for key in ("tests", "skipped", "failures", "errors")}


def _project_command(command: list[str]) -> list[str]:
    """Run Python gates in the project environment, including when launched by uv."""
    if command and Path(command[0]).name.lower().startswith("python") and shutil.which("uv"):
        extras = []
        joined = " ".join(command[1:])
        if "pytest" in joined:
            extras.append("pytest")
        if any(name in joined for name in ("assets_gate", "art_contact", "art_review", "pytest_gate")):
            extras.append("Pillow")
        return ["uv", "run", *(sum((["--with", package] for package in extras), [])), "python", *command[1:]]
    return command


def run_gate(name: str) -> dict:
    print(f"release candidate: running {name}", flush=True)
    result = release_gate.run(name, _project_command(release_gate.GATES[name]))
    print(f"release candidate: {name}={result['status']}", flush=True)
    return result


def main() -> int:
    started = datetime.now(timezone.utc).isoformat()
    source = identity()
    results = [run_gate(name) for name in ORDER]
    # Live evidence is never inherited from a prior report. It is either
    # generated in this invocation or explicitly recorded as blocked.
    live = {}
    live_names = ("genie-eval", "deployed-smoke", "deployed-soak")
    if os.getenv("RUN_LIVE_GATES") == "1":
        commands = {
            "genie-eval": [sys.executable, "scripts/live_genie_check.py"],
            "deployed-smoke": [sys.executable, "scripts/deployed_smoke.py"],
            "deployed-soak": [sys.executable, "scripts/deployed_soak.py"],
        }
        for name in live_names:
            print(f"release candidate: running {name}", flush=True)
            item = release_gate.run(name, _project_command(commands[name]))
            print(f"release candidate: {name}={item['status']}", flush=True)
            item["source_identity"] = source
            live[name] = item
    else:
        for name in live_names:
            live[name] = {"name": name, "status": "BLOCKED_EXTERNAL", "reason": "RUN_LIVE_GATES=1 is required; stale PASS evidence is never reused"}
    final_source = identity()
    identity_match = source["commit_sha"] == final_source["commit_sha"] and source["tree_sha"] == final_source["tree_sha"]
    failed = [item["name"] for item in results if item["status"] != "PASS"]
    failed += [name for name, item in live.items() if item["status"] != "PASS"]
    if not identity_match:
        failed.append("source-identity-stability")
    blockers = [name for name, item in live.items() if item["status"] == "BLOCKED_EXTERNAL"]
    summary = {
        "status": "PASS" if not failed else "FAIL",
        "generated_at_utc": started,
        "source_identity": source,
        "identity_stable": identity_match,
        "build_identity": {"runtime_digest": source["runtime_digest"], "data_contract_digest": source["data_contract_digest"]},
        "test_counts": test_counts(),
        "gates": results,
        "genie_result": live["genie-eval"],
        "deployment_result": live["deployed-smoke"],
        "soak_result": live["deployed-soak"],
        "asset_sha256": asset_hashes(),
        "unresolved_external_human_blockers": blockers,
        "failed_requirements": failed,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "commit_sha": source["commit_sha"], "tree_sha": source["tree_sha"], "failed": failed}, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
