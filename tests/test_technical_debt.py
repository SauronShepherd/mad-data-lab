from pathlib import Path

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
