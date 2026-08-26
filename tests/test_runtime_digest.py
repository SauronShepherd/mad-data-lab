import subprocess, sys
from pathlib import Path

from scripts.compute_runtime_digest import files


ROOT = Path(__file__).resolve().parents[1]


def test_runtime_digest_is_deterministic():
    a = subprocess.check_output([sys.executable, 'scripts/compute_runtime_digest.py'], cwd=ROOT, text=True).strip()
    b = subprocess.check_output([sys.executable, 'scripts/compute_runtime_digest.py'], cwd=ROOT, text=True).strip()
    assert len(a) == 64 and a == b


def test_runtime_digest_file_set_includes_genie_contract_and_case_catalog():
    paths = {path.relative_to(ROOT).as_posix() for path in files()}
    assert "genie/instructions.md" in paths
    assert "genie/registry.json" in paths
    assert "genie/agent.source.json" in paths
    assert "cases/catalog.yaml" in paths
