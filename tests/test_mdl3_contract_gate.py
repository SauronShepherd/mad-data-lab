import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_mdl3_contract_gate_passes_and_writes_digest_artifact():
    result = subprocess.run([sys.executable, "scripts/validate_mdl3_contract.py", "--strict"], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    artifact = json.loads((ROOT / "release-report/MDL-3/contract-validation.json").read_text(encoding="utf-8"))
    assert artifact["status"] == "PASS"
    assert len(artifact["genie_contract_digest"]) == 64
