from __future__ import annotations
import argparse, json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data.generation import generate_case

def main():
    p=argparse.ArgumentParser(); p.add_argument('--manifest', required=True); p.add_argument('--target', default='staging'); p.add_argument('--apply', action='store_true'); a=p.parse_args()
    if a.target != 'staging': raise SystemExit('rollback target must be staging')
    m=json.loads(Path(a.manifest).read_text(encoding='utf-8')); c=generate_case(m['case_id'])
    if c.content_hash != m['canonical_case_hash']: raise SystemExit('rollback manifest does not match repository source')
    if m.get('public_bundle') and m['public_bundle'] != c.public: raise SystemExit('rollback public snapshot differs from repository source')
    if not a.apply: print(json.dumps({'mode':'plan','case_id':m['case_id'],'hash':c.content_hash})); return
    raise SystemExit('remote rollback requires an authenticated staging SQL resource')
if __name__=='__main__': main()
