import subprocess
import sys
import csv
import json
from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_mdl6_coverage_matrix_is_complete_and_does_not_overclaim():
    result = subprocess.run(
        [sys.executable, "scripts/mdl6_coverage_matrix.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["total"] == 94
    assert payload["implemented"] == 94
    assert payload["partial"] == 0
    assert payload["not_implemented"] == 0
    assert payload["acceptance_policy"] == {
        "ci": "NOT_APPLICABLE",
        "human_approval": "NOT_APPLICABLE",
        "authoritative_validation": ["local tests", "Databricks CLI profile mdl"],
    }
    required_fields = {"id", "implementation", "unit_test", "integration_test", "e2e_test",
                       "remote_validation", "acceptance_criteria", "status", "blocker"}
    required_fields |= {"ci_validation", "human_approval"}
    assert all(required_fields <= set(row) for row in payload["scenarios"])
    assert all(row["acceptance_criteria"] for row in payload["scenarios"])
    assert all(row["test"] for row in payload["scenarios"] if row["status"] == "PASS_IMPLEMENTED")


def test_csv_traceability_is_synchronized_with_matrix():
    with (ROOT / "docs/traceability/mdl6-requirements.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    expected = {row["id"] for row in json.loads(subprocess.run(
        [sys.executable, "scripts/mdl6_coverage_matrix.py"], cwd=ROOT,
        capture_output=True, text=True).stdout)["scenarios"]}
    assert {row["id"] for row in rows} == expected
    required = {"id", "implementation", "unit_test", "integration_test", "e2e_test",
                "remote_validation", "acceptance_criteria", "status", "blocker"}
    required |= {"ci_validation", "human_approval"}
    assert required <= set(rows[0])
