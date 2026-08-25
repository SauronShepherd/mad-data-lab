from __future__ import annotations
import argparse, json, os, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data.generation import generate_case

def main():
    p=argparse.ArgumentParser(); p.add_argument('--target', choices=('local','staging'), default='local'); p.add_argument('--case-id', default='CASE_0042'); p.add_argument('--profile', default=''); p.add_argument('--warehouse-id', default=os.getenv('MDL_WAREHOUSE_ID','')); p.add_argument('--catalog', default=os.getenv('MDL_CATALOG','')); a=p.parse_args()
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
    result={'status':'LOCAL_CANONICAL_ONLY','case_id':a.case_id,'canonical_case_hash':c.content_hash,'snapshot_counts':counts,'public_truth_excluded':'private' not in bundle}
    if a.target == 'staging':
        if not a.profile or not a.warehouse_id or not a.catalog:
            raise SystemExit('staging verification requires --profile, --warehouse-id, and --catalog')
        env=os.environ.copy(); env['MDL_CATALOG']=a.catalog; env['MDL_WAREHOUSE_ID']=a.warehouse_id
        completed=subprocess.run([sys.executable,'scripts/live_sql_check.py','--profile',a.profile,'--warehouse-id',a.warehouse_id,'--case-id',a.case_id], cwd=Path(__file__).resolve().parents[1], env=env, capture_output=True, text=True)
        if completed.returncode:
            raise SystemExit('staging verification failed: ' + (completed.stdout + completed.stderr)[-4000:])
        result['status']='REMOTE_SQL_VERIFIED'; result['profile']=a.profile; result['catalog']=a.catalog; result['warehouse_id']=a.warehouse_id
    print(json.dumps(result, sort_keys=True))
if __name__=='__main__': main()
