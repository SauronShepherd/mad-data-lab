"""Materialize the named public evidence fixtures from the canonical bundle."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "data/fixtures/public"

MAPPING = {
    "case_0042_component_evidence.json": "calculation_trace",
    "case_0042_snapshot_evidence.json": "snapshot_diff",
    "case_0042_quality_evidence.json": "quality_issues",
    "case_0042_semantic_evidence.json": "semantic_evidence",
    "case_0042_lineage_evidence.json": "technical_lineage",
}


def main() -> None:
    bundle = json.loads((PUBLIC / "case_0042.bundle.json").read_text(encoding="utf-8"))
    for filename, key in MAPPING.items():
        payload = {
            "case_id": "CASE_0042",
            "fixture_type": key,
            "records": bundle[key],
        }
        (PUBLIC / filename).write_text(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    print(f"materialized {len(MAPPING)} public fixtures")


if __name__ == "__main__":
    main()
