import subprocess,sys
from pathlib import Path
def test_g42_traceability_is_unique_and_complete():
    r=subprocess.run([sys.executable,'scripts/validate_traceability.py'],cwd=Path(__file__).parents[1],capture_output=True,text=True)
    assert r.returncode==0,r.stdout+r.stderr
