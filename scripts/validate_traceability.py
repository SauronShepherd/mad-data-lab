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
    result={'status':'PASS' if not missing and not duplicates else 'FAIL','required_ids':len(required),'definitions':len(ids),'missing':missing,'duplicates':duplicates}
    print(json.dumps(result,indent=2));
    if missing or duplicates: raise SystemExit(1)
if __name__=='__main__': main()
