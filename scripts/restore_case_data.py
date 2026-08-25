from __future__ import annotations
import argparse, json, os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data.generation import generate_case
from backend.data.sql_client import connect_from_env, execute_native, configured_object, validate_case_id, SqlAdapterError

PUBLIC_TABLES = ('case_definition','datapoint_result','calculation_trace','source_snapshot','source_record','snapshot_diff','quality_issue','pipeline_run_evidence','semantic_change_evidence','technical_lineage_curated')

def main():
    p=argparse.ArgumentParser(); p.add_argument('--manifest', required=True); p.add_argument('--target', default='staging'); p.add_argument('--apply', action='store_true'); a=p.parse_args()
    if a.target != 'staging': raise SystemExit('rollback target must be staging')
    m=json.loads(Path(a.manifest).read_text(encoding='utf-8')); validate_case_id(m['case_id']); c=generate_case(m['case_id'])
    if c.content_hash != m['canonical_case_hash']: raise SystemExit('rollback manifest does not match repository source')
    if m.get('public_bundle') and m['public_bundle'] != c.public: raise SystemExit('rollback public snapshot differs from repository source')
    backups=m.get('backup_tables') or {}
    if not a.apply: print(json.dumps({'mode':'plan','case_id':m['case_id'],'hash':c.content_hash,'backup_tables':backups})); return
    catalog=os.environ.get('MDL_CATALOG')
    if not catalog or set(backups) != set(PUBLIC_TABLES): raise SystemExit('staging rollback requires a complete snapshot manifest and MDL_CATALOG')
    try:
        with connect_from_env() as connection:
            with connection.cursor() as cursor:
                for table in PUBLIC_TABLES:
                    target=configured_object(catalog,'mad_data_lab_public',table)
                    backup=backups[table]
                    execute_native(cursor, f"DELETE FROM {target} WHERE case_id = ?", (m['case_id'],))
                    execute_native(cursor, f"INSERT INTO {target} SELECT * FROM {backup}", ())
    except SqlAdapterError as exc: raise SystemExit(f'restore: NOT RUN ({exc})') from exc
    print(json.dumps({'mode':'apply','case_id':m['case_id'],'hash':c.content_hash,'restored_tables':list(PUBLIC_TABLES)}))
if __name__=='__main__': main()
