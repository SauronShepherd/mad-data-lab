import subprocess, sys
from pathlib import Path

def test_runtime_digest_is_deterministic():
    root=Path(__file__).parents[1]
    a=subprocess.check_output([sys.executable,'scripts/compute_runtime_digest.py'],cwd=root,text=True).strip()
    b=subprocess.check_output([sys.executable,'scripts/compute_runtime_digest.py'],cwd=root,text=True).strip()
    assert len(a)==64 and a==b
