import subprocess, sys
from pathlib import Path
def test_mdl2_contract_validator_passes_in_progress_mode():
    root=Path(__file__).parents[1]
    result=subprocess.run([sys.executable,'scripts/validate_mdl2_contract.py'],cwd=root,capture_output=True,text=True)
    assert result.returncode==0,result.stdout+result.stderr

def test_mdl2_art_candidate_slots_are_complete_and_stable():
    import json
    preflight=json.loads((Path(__file__).parents[1]/'release-report'/'MDL-2'/'art-preflight.json').read_text())
    ids={item['candidate_id'] for item in preflight['candidates']}
    assert ids == {f'A{asset:02d}-C{candidate:02d}' for asset in range(8,13) for candidate in range(1,4)}
