"""Fail-closed checks for the browser package's analytical trust boundary."""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]
def main():
    source = '\n'.join(p.read_text(encoding='utf-8', errors='ignore') for p in ROOT.glob('src/**/*') if p.is_file())
    forbidden = ('primary_cause', 'truth_json', 'expected_path_json', 'allowed_final_status_json', 'Promo effect?', 'EXP-01', 'EXP-02', 'EXP-03')
    for marker in forbidden:
        assert marker not in source, f'forbidden analytical fixture in frontend source: {marker}'
    dist = ROOT / 'dist'
    if dist.exists():
        built = '\n'.join(p.read_text(encoding='utf-8', errors='ignore') for p in dist.rglob('*') if p.is_file() and p.suffix in {'.js','.html','.css'})
        for marker in ('primary_cause', 'truth_json', 'expected_path_json', 'Promo effect?', 'EXP-01'):
            assert marker not in built, f'private/legacy marker in built frontend: {marker}'
    assert 'startInvestigation' in source and 'getNextExperiment' in source
    print('frontend contract gate: PASS')
if __name__ == '__main__':
    try: main()
    except AssertionError as exc: print(f'frontend contract gate: FAIL: {exc}', file=sys.stderr); raise SystemExit(1)
