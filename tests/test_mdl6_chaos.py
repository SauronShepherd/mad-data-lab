from pathlib import Path
import subprocess
import sys


def test_local_chaos_harness_asserts_recovery_contract():
    result = subprocess.run([sys.executable, "scripts/local_chaos.py"], cwd=Path(__file__).parents[1], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "fails closed" in result.stdout
