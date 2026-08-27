import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_mdl5_traceability_rows_are_complete_and_evidence_bound():
    rows = list(csv.DictReader((ROOT / "docs/traceability/mdl5-requirements.csv").open(encoding="utf-8")))
    assert len(rows) == 25
    assert len({row["requirement_id"] for row in rows}) == len(rows)
    for row in rows:
        assert row["implementation"] and row["tests"] and row["release_evidence"]
        assert row["status"] in {"implemented", "partial", "pending"}
        for path in row["implementation"].split(";") + row["tests"].split(";"):
            target = ROOT / path
            if path == "manual review":
                continue
            assert target.exists() or (row["status"] == "pending" and path.endswith("/")), f"missing traceability path: {path}"


def test_mdl5_manifest_is_separate_from_mdl4_and_has_required_identity_fields():
    manifest = json.loads((ROOT / "release-report/MDL-5/manifest.json").read_text())
    assert manifest["iteration"] == "MDL-5"
    assert manifest["predecessor"]["accepted_sha"] == "f7d2f4d7255373bbed4d036561ea2ff3342ba4a7"
    assert (ROOT / "release-report/MDL-4/manifest.json").exists()
    assert json.loads((ROOT / "release-report/MDL-4/manifest.json").read_text())["iteration"] == "MDL-4"
