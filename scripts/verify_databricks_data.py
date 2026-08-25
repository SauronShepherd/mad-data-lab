from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data.generation import generate_case

def main():
    p=argparse.ArgumentParser(); p.add_argument('--target', default='local'); p.add_argument('--case-id', default='CASE_0042'); a=p.parse_args()
    if a.target not in ('local','staging'): raise SystemExit('unknown target; refusing verification')
    c=generate_case(a.case_id)
    public_path=Path('data/fixtures/public/case_0042.bundle.json')
    bundle=json.loads(public_path.read_text(encoding='utf-8'))
    if bundle != c.canonical: raise SystemExit('public fixture differs from generated canonical package')
    rows=c.canonical['snapshot_diff']
    counts={kind:sum(1 for row in rows if row['change_type']==kind) for kind in ('MODIFIED','REMOVED','ADDED')}
    current_records=[row for row in c.canonical['source_records'] if row['snapshot_id']=='SNAP_20260803_0900']
    counts['UNCHANGED']=sum(1 for row in current_records if row['changed_from_previous'] is False and row['component']=='V2')
    if counts != {'MODIFIED':23,'REMOVED':2,'ADDED':5,'UNCHANGED':14}: raise SystemExit(f'wrong snapshot counts: {counts}')
    print(json.dumps({'status':'LOCAL_CANONICAL_ONLY' if a.target=='local' else 'REMOTE_NOT_RUN','case_id':a.case_id,'canonical_case_hash':c.content_hash,'snapshot_counts':counts,'public_truth_excluded':'private' not in bundle}, sort_keys=True))
if __name__=='__main__': main()
