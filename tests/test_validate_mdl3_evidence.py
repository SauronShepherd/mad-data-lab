import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def artifact():
    return {
        "implementation_sha": "impl",
        "genie_contract_digest": "contract",
        "genie_live_config_sha256": "live",
        "mdl2_data_contract_digest": "data",
        "case_hash": "case",
        "batch_id": "batch-1",
        "status": "PASS",
        "attempts": [{"benchmark_id": benchmark_id(i), "status": "PASS"} for i in range(30)],
    }


def benchmark_id(i):
    groups = [("OBS", 3), ("CMP", 3), ("SNP", 3), ("DQ", 3), ("FOR", 3), ("LIN", 2), ("GSTART", 5), ("GNEXT", 5), ("SEC", 3)]
    for prefix, count in groups:
        if i < count:
            return f"{prefix}-{i + 1:02d}"
        i -= count
    raise AssertionError(i)


def args(path: Path):
    return [sys.executable, "scripts/validate_mdl3_evidence.py", str(path), "--implementation-sha", "impl", "--genie-contract-digest", "contract", "--genie-live-config-sha256", "live", "--mdl2-data-contract-digest", "data", "--case-hash", "case"]


def test_cli_accepts_current_artifact(tmp_path: Path):
    path = tmp_path / "evidence.json"
    path.write_text(json.dumps(artifact()), encoding="utf-8")
    result = subprocess.run(args(path), cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


def test_cli_rejects_stale_artifact(tmp_path: Path):
    path = tmp_path / "evidence.json"
    value = artifact()
    value["genie_contract_digest"] = "stale"
    path.write_text(json.dumps(value), encoding="utf-8")
    result = subprocess.run(args(path), cwd=ROOT, capture_output=True, text=True)
    assert result.returncode != 0
    assert "FAIL" in result.stdout
