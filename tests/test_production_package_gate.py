import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_production_package_gate_passes():
    result = subprocess.run([sys.executable, "scripts/production_package_gate.py"], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["status"] == "PASS"


def test_production_package_gate_rejects_private_paths_and_markers(tmp_path):
    (tmp_path / "data/generation/private_specs").mkdir(parents=True)
    (tmp_path / "data/generation/private_specs/case.yaml").write_text("primary_cause: hidden", encoding="utf-8")
    result = subprocess.run([sys.executable, "scripts/production_package_gate.py", "--package-root", str(tmp_path)], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["status"] == "FAIL"
    assert any("forbidden path" in item for item in payload["failures"])
