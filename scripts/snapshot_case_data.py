from __future__ import annotations
import argparse, json, sys
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data.generation import generate_case

def main():
    p=argparse.ArgumentParser(); p.add_argument('--output', default='release-report/MDL-2/rollback-before.json'); p.add_argument('--case-id', default='CASE_0042'); a=p.parse_args()
    c=generate_case(a.case_id); out=Path(a.output); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({'case_id':a.case_id,'captured_at_utc':datetime.now(timezone.utc).isoformat(),'canonical_case_hash':c.content_hash,'public_bundle':c.public,'state':'KNOWN_GOOD_SOURCE'}, sort_keys=True, indent=2), encoding='utf-8')
    print(out)
if __name__=='__main__': main()
