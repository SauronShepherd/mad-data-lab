from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_mdl4_manifest_generator_records_predecessor_and_current_identity():
    result = subprocess.run([sys.executable, "scripts/generate_mdl4_manifest.py"], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads((ROOT / "release-report/MDL-4/manifest.json").read_text())
    assert data["iteration"] == "MDL-4"
    assert data["branch"] == "MDL-4"
    assert len(data["base_commit_sha"]) == 40
    assert len(data["base_tree_sha"]) == 40
    assert len(data["accepted_head_commit_sha"]) == 40
    assert len(data["accepted_head_tree_sha"]) == 40
    assert len(data["asset_sha256"]) == 10


def test_mdl4_manifest_closure_validator_is_fail_closed():
    result = subprocess.run(
        [sys.executable, "scripts/validate_iteration_manifest.py", "release-report/MDL-4/manifest.json", "--require-complete"],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert result.returncode != 0
    assert "open_blockers" in result.stdout
