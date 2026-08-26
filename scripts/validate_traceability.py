from __future__ import annotations
import csv, json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    rows=list(csv.DictReader((ROOT/'docs/traceability/mdl2-tests.csv').open(encoding='utf-8')))
    ids=[r['test_id'] for r in rows]; counts=Counter(ids)
    required=(
        [f'G42-{i:03d}' for i in range(1,28)]
        + [f'DG-{i:03d}' for i in range(1,11)]
        + [f'DP-{i:03d}' for i in range(1,21)]
        + [f'SQ-{i:03d}' for i in range(1,21)]
    )
    missing=[x for x in required if counts[x]!=1]; duplicates=sorted(x for x,n in counts.items() if n>1)
    section_path = ROOT / 'docs/traceability/v3-section-coverage.csv'
    sections = list(csv.DictReader(section_path.open(encoding='utf-8'))) if section_path.is_file() else []
    section_numbers = [row.get('section', '') for row in sections]
    section_error = (
        len(sections) != 54
        or section_numbers != [str(number) for number in range(1, 55)]
        or any(row.get('source_version') != '3.0' or not row.get('primary_owner') or not row.get('status') for row in sections)
    )
    result={'status':'PASS' if not missing and not duplicates and not section_error else 'FAIL','required_ids':len(required),'definitions':len(ids),'missing':missing,'duplicates':duplicates,'v3_sections':len(sections),'v3_section_error':section_error}
    print(json.dumps(result,indent=2));
    if missing or duplicates or section_error: raise SystemExit(1)
if __name__=='__main__': main()
