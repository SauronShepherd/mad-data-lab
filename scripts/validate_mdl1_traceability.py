"""Validate the honest MDL-1 evidence ledger."""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "MDL1-ARCH-001", "MDL1-ARCH-002", "MDL1-API-001", "MDL1-CI-001",
    "MDL1-CI-002", "MDL1-CI-003", "MDL1-DEP-001", "MDL1-DATA-001",
    "MDL1-ART-001", "MDL1-PRE-001",
}
STATUSES = {"PASS", "PASS_LOCAL", "PASS_REMOTE", "PENDING", "BLOCKED"}


def main() -> None:
    path = ROOT / "docs/traceability/mdl1-tests.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    counts = Counter(row["test_id"] for row in rows)
    missing = sorted(REQUIRED - set(counts))
    duplicate = sorted(test_id for test_id, count in counts.items() if count != 1)
    invalid = sorted(row["test_id"] for row in rows if row["status"] not in STATUSES)
    result = {"status": "PASS" if not missing and not duplicate and not invalid else "FAIL", "rows": len(rows), "missing": missing, "duplicate": duplicate, "invalid_status": invalid, "pending": sorted(row["test_id"] for row in rows if row["status"] in {"PENDING", "BLOCKED"})}
    print(json.dumps(result, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
