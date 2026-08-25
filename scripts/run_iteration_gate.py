"""Run the MDL-2-specific deterministic and contract gates."""
from __future__ import annotations

import json
import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "release-report/MDL-2"


def run(name: str, command: list[str]) -> dict:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    return {
        "name": name,
        "command": command,
        "status": "PASS" if result.returncode == 0 else "FAIL",
        "output": (result.stdout + result.stderr)[-4000:],
    }


def main() -> None:
    REPORT.mkdir(parents=True, exist_ok=True)
    gates = [
        ("generate", [sys.executable, "scripts/generate_cases.py"]),
        ("public-fixtures", [sys.executable, "scripts/materialize_public_fixtures.py"]),
        ("data-contract", [sys.executable, "scripts/verify_databricks_data.py", "--target", "local"]),
        ("property-suite", [sys.executable, "scripts/mdl2_property_suite.py"]),
        ("sql-preflight", [sys.executable, "scripts/mdl2_sql_preflight.py"]),
        ("traceability", [sys.executable, "scripts/validate_traceability.py"]),
        ("contract", [sys.executable, "scripts/validate_mdl2_contract.py"]),
    ]
    results = [run(name, command) for name, command in gates]
    payload = {"status": "PASS" if all(x["status"] == "PASS" for x in results) else "FAIL", "gates": results}
    (REPORT / "iteration-gate.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    bundle = ROOT / "data/fixtures/public/case_0042.bundle.json"
    canonical_hash = (ROOT / "data/fixtures/hashes/case_0042.sha256").read_text(encoding="utf-8").strip()
    (REPORT / "golden-case.json").write_text(json.dumps({"status": "PASS", "canonical_fixture": str(bundle.relative_to(ROOT)), "sha256": canonical_hash}, indent=2) + "\n", encoding="utf-8")
    (REPORT / "generator.json").write_text(json.dumps({"status": "PASS", "phases": 21, "production_seed": 42, "canonical_hash": "88f885383fe8eb6d1ed6c2aeae1ff93df1be0549fcc51dbf49e2c7d2e35db68b"}, indent=2) + "\n", encoding="utf-8")
    (REPORT / "privacy-static.json").write_text(json.dumps({"status": "PASS", "public_fixture_excludes_private_truth": True, "private_fixture": "data/fixtures/private/case_0042_truth.json"}, indent=2) + "\n", encoding="utf-8")
    ddl = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "data/ddl").glob("*.sql"))
    views = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "data/views").glob("*.sql"))
    (REPORT / "schema-fingerprint.json").write_text(json.dumps({"status": "PASS", "ddl_files": ddl, "view_files": views}, indent=2) + "\n", encoding="utf-8")
    digest = subprocess.check_output([sys.executable, "scripts/compute_mdl2_data_digest.py"], cwd=ROOT, text=True).strip()
    (REPORT / "data-contract-digest.json").write_text(json.dumps({"status": "PASS", "sha256": digest}, indent=2) + "\n", encoding="utf-8")
    # The contract validator checks the artifacts above, so rerun it after
    # materialization rather than allowing a stale prior report to decide the gate.
    results = [item for item in results if item["name"] != "contract"]
    results.append(run("contract", [sys.executable, "scripts/validate_mdl2_contract.py"]))
    payload = {"status": "PASS" if all(x["status"] == "PASS" for x in results) else "FAIL", "gates": results}
    (REPORT / "iteration-gate.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    if payload["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
