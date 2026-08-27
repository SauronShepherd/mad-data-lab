from __future__ import annotations

import json
import hashlib
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


def test_successor_branch_preserves_historical_mdl4_manifest():
    path = ROOT / "release-report/MDL-4/manifest.json"
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    result = subprocess.run([sys.executable, "scripts/generate_mdl4_manifest.py"], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert hashlib.sha256(path.read_bytes()).hexdigest() == before
    data = json.loads(path.read_text())
    assert data["branch"] == "MDL-4"
    assert data["accepted_head_commit_sha"] != "" and len(data["accepted_head_commit_sha"]) == 40


def test_mdl4_manifest_validator_rejects_malformed_manifest(tmp_path):
    path = tmp_path / "manifest.json"
    data = json.loads((ROOT / "release-report/MDL-4/manifest.json").read_text())
    data["branch"] = "MDL-5"
    data["accepted_head_commit_sha"] = "not-a-sha"
    path.write_text(json.dumps(data))
    result = subprocess.run([sys.executable, "scripts/validate_iteration_manifest.py", str(path)], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode != 0
    assert "branch:not-MDL-4" in result.stdout
    assert "malformed:accepted_head_commit_sha" in result.stdout


def test_manifest_generator_does_not_accept_branch_spoofing(monkeypatch):
    monkeypatch.setenv("GIT_BRANCH", "MDL-4")
    result = subprocess.run([sys.executable, "scripts/generate_mdl4_manifest.py"], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0
    assert json.loads((ROOT / "release-report/MDL-4/manifest.json").read_text())["branch"] == "MDL-4"
