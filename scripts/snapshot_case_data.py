from __future__ import annotations
import argparse, json, os, sys
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data.generation import generate_case
from backend.data.sql_client import connect_from_env, execute_native, configured_object, validate_case_id, SqlAdapterError

PUBLIC_TABLES = ('case_definition','datapoint_result','calculation_trace','source_snapshot','source_record','snapshot_diff','quality_issue','pipeline_run_evidence','semantic_change_evidence','technical_lineage_curated')

def main():
    p=argparse.ArgumentParser(); p.add_argument('--output', default='release-report/MDL-2/rollback-before.json'); p.add_argument('--case-id', default='CASE_0042'); p.add_argument('--target', choices=('local','staging'), default='local'); a=p.parse_args()
    validate_case_id(a.case_id)
    c=generate_case(a.case_id); out=Path(a.output); out.parent.mkdir(parents=True, exist_ok=True)
    payload={'case_id':a.case_id,'captured_at_utc':datetime.now(timezone.utc).isoformat(),'canonical_case_hash':c.content_hash,'public_bundle':c.public,'state':'KNOWN_GOOD_SOURCE','target':'local','backup_tables':{}}
    if a.target == 'staging':
        catalog = os.environ.get('MDL_CATALOG')
        if not catalog: raise SystemExit('staging snapshot requires MDL_CATALOG')
        try:
            with connect_from_env() as connection:
                with connection.cursor() as cursor:
                    for table in PUBLIC_TABLES:
                        source = configured_object(catalog, 'mad_data_lab_public', table)
                        backup = configured_object(catalog, 'mad_data_lab_public', f'mdl2_rollback_{a.case_id.lower()}_{table}')
                        execute_native(cursor, f"CREATE OR REPLACE TABLE {backup} AS SELECT * FROM {source} WHERE case_id = ?", (a.case_id,))
                        payload['backup_tables'][table] = backup
            payload['target'] = 'staging'
        except SqlAdapterError as exc: raise SystemExit(f'snapshot: NOT RUN ({exc})') from exc
    out.write_text(json.dumps(payload, sort_keys=True, indent=2), encoding='utf-8')
    print(out)
if __name__=='__main__': main()
