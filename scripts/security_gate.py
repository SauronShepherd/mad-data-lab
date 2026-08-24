"""Local static security gate for synthetic-data and closed-control invariants."""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    source_files = [*ROOT.glob("server/**/*.py"), *ROOT.glob("src/**/*"), *ROOT.glob("resources/**/*.json"), *ROOT.glob("sql/**/*.sql")]
    source = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in source_files if path.is_file())
    assert not re.search(r"(?i)(databricks_pat|api[_-]?key|client_secret|password\s*=)", source), "secret-like source pattern found"
    frontend = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in ROOT.glob("src/**/*") if path.is_file())
    assert "CASE_TRUTH" not in frontend and "primary_component" not in frontend
    assert "eval(" not in frontend and "new Function(" not in frontend
    assert "case_id" in source and "registered" in source
    print("security gate: PASS")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(f"security gate: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
