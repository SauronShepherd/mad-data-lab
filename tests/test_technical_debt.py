from pathlib import Path
import json
import subprocess

import yaml

from server.catalog import FULL_CASE_CATALOG, case_availability


ROOT = Path(__file__).resolve().parents[1]


def test_catalog_projection_is_not_an_entitlement_source():
    public = yaml.safe_load((ROOT / "cases/catalog.yaml").read_text(encoding="utf-8"))
    canonical_ids = {item["id"] for item in public["cases"]}
    assert canonical_ids == {"CASE_0042", "CASE_0107"}
    assert [case.id for case in FULL_CASE_CATALOG if case_availability(case) == "AVAILABLE"] == ["CASE_0042"]
    assert all(case_availability(case) == "LOCKED" for case in FULL_CASE_CATALOG if case.id != "CASE_0042")


def test_debt_ledger_has_no_unexplained_open_items():
    text = (ROOT / "docs/iterations/technical-debt.md").read_text(encoding="utf-8")
    assert "| OPEN |" not in text
    for line in text.splitlines():
        if line.startswith("| TD-"):
            assert "rationale:" in line or "CLOSED" in line or "BLOCKED_" in line


def test_td005_closure_is_bound_to_real_historical_live_evidence():
    manifest = json.loads((ROOT / "release-report/MDL-4/manifest.json").read_text(encoding="utf-8"))
    external = json.loads((ROOT / "release-report/MDL-4/external-evidence.json").read_text(encoding="utf-8"))
    session = json.loads((ROOT / "release-report/MDL-4/live-session.json").read_text(encoding="utf-8"))
    accepted = manifest["accepted_head_commit_sha"]
    assert len(accepted) == 40
    assert subprocess.run(["git", "cat-file", "-e", f"{accepted}^{{commit}}"], cwd=ROOT).returncode == 0
    assert manifest["databricks_deployment"]["deployment_or_run_id"] == external["live-deployment"]["immutable_id"]
    assert session["status"] == "PASS" and session["health"] == "ok" and session["score"] == 1000
    assert session["started_at"] < session["finished_at"]
