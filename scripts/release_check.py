"""Fast local release gate for the MAD DATA LAB challenge build."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from server.catalog import get_case


def require_file(relative: str) -> None:
    path = ROOT / relative
    if not path.is_file() or path.stat().st_size == 0:
        raise AssertionError(f"missing or empty required artifact: {relative}")


def main() -> None:
    for artifact in (
        "app.yaml",
        "assets/review/MDL-2/art-generation-plan.json",
        "release-report/MDL-2/art-preflight.json",
        "resources/genie/case_0042.serialized.json",
        "databricks.yml",
    ):
        require_file(artifact)

    app_yaml = (ROOT / "app.yaml").read_text(encoding="utf-8")
    assert "genie-space" in app_yaml and "server.run" in app_yaml
    launcher = (ROOT / "server/run.py").read_text(encoding="utf-8")
    assert "UVICORN_HOST" in launcher and "UVICORN_PORT" in launcher

    serialized = json.loads((ROOT / "resources/genie/case_0042.serialized.json").read_text(encoding="utf-8"))
    identifiers = [item["identifier"] for item in serialized["data_sources"]["tables"]]
    assert len(identifiers) >= 5
    assert identifiers == sorted(identifiers), "Genie table identifiers must be lexicographically sorted"

    case = get_case("CASE_0042")
    assert case.state == "CORE"
    assert case.required_experiments == ("COMPONENT_DECOMPOSITION", "SNAPSHOT_DIFF", "DQ_MATERIALITY", "FORMULA_VALIDATION", "RECONCILIATION")
    print("MAD DATA LAB release gate: PASS")


if __name__ == "__main__":
    main()
