"""Generate/apply an idempotent, case-scoped MDL-2 public migration."""
from __future__ import annotations
import argparse, json, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data.generation import generate_case
from backend.data.sql_client import connect_from_env, execute_native, SqlAdapterError

ROOT=Path(__file__).resolve().parents[1]
def lit(value):
    if value is None: return 'NULL'
    if isinstance(value,bool): return 'TRUE' if value else 'FALSE'
    if isinstance(value,(int,float)): return str(value)
    return "'"+str(value).replace("'","''")+"'"

def migration(catalog, case):
    public=f'{catalog}.mad_data_lab_public'; p=case.public; c=case.canonical; statements=[]
    def insert(table, columns, rows):
        values = [f"({','.join(lit(row.get(column)) for column in columns)})" for row in rows]
        if values:
            statements.append(f"INSERT INTO {public}.{table} ({','.join(columns)}) VALUES {','.join(values)};")
    statements.append(f"DELETE FROM {public}.case_definition WHERE case_id = 'CASE_0042';")
    statements.append(f"INSERT INTO {public}.case_definition (case_id, public_number, title, expected_value, observed_value, deviation, generator_version, case_template_version, created_at, status) VALUES ('CASE_0042',42,{lit(p['title'])},125.00,118.20,-6.80,{p['generator_version']},{p['case_template_version']},TIMESTAMP '2026-08-03 09:00:00','ACTIVE');")
    statements.append(f"DELETE FROM {public}.snapshot_diff WHERE case_id = 'CASE_0042';")
    for row in p['snapshot_evidence']:
        statements.append(f"INSERT INTO {public}.snapshot_diff (case_id, component, business_key, change_type, old_value, new_value, impact, current_snapshot_id) VALUES ('CASE_0042',{lit(row['component'])},{lit(row['business_key'])},{lit(row['change_type'])},{lit(row['old_value'])},{lit(row['new_value'])},{lit(row['impact'])},'SNAP_20260803_0900');")
    statements.append(f"DELETE FROM {public}.quality_issue WHERE case_id = 'CASE_0042';")
    q=p['quality_evidence'][0]
    statements.append(f"INSERT INTO {public}.quality_issue (case_id, issue_id, rule_name, affected_keys, affected_row_count, estimated_impact, impact_is_overlapping, status) VALUES ('CASE_0042','DQ_0042_01','DUPLICATE_BUSINESS_KEY',{lit(json.dumps(q['affected_keys'],separators=(',',':')))},5,-0.30,TRUE,'OPEN');")
    statements.extend([f"DELETE FROM {public}.{table} WHERE case_id = 'CASE_0042';" for table in ('datapoint_result','calculation_trace','source_snapshot','source_record','semantic_change_evidence','pipeline_run_evidence','technical_lineage_curated')])
    insert('datapoint_result', ('case_id','datapoint_id','entity_id','period_id','run_id','run_ts','run_role','value','expected_value','deviation','formula_id','formula_hash','filter_id','filter_hash','population_hash'), [dict(row, entity_id='PT001', period_id='2026-07', value=row['observed_value'], filter_id=p['filter_id'], filter_hash=p['filter_hash']) for row in c['datapoint_results']])
    trace=[]
    for index, component in enumerate(p['component_evidence'], start=1):
        trace.append({'case_id':'CASE_0042','datapoint_id':'CAPITAL_AVAILABLE','run_id':'RUN_0042_20260803_0900','parent_node_id':'CAPITAL_AVAILABLE','node_id':component['component'],'node_type':'COMPONENT','label':component['component'],'operation':'COMPONENT_DELTA','formula':None,'value':component['current_value'],'previous_value':component['previous_value'],'contribution_delta':component['contribution_delta'],'source_table':'finance_reporting_source','source_column':'amount','filters_json':None,'join_json':None,'snapshot_id':'SNAP_20260803_0900','sequence_no':index})
    insert('calculation_trace', ('case_id','datapoint_id','run_id','parent_node_id','node_id','node_type','label','operation','formula','value','previous_value','contribution_delta','source_table','source_column','filters_json','join_json','snapshot_id','sequence_no'), trace)
    snapshots=[{'snapshot_id':x['snapshot_id'],'case_id':'CASE_0042','source_table':'finance_reporting_source','as_of_ts':x['run_ts'],'row_count':x['row_count'],'status':'SUCCESS','snapshot_role':x['role'],'pipeline_run_id':x['run_id']} for x in c['source_snapshots']]
    insert('source_snapshot', tuple(snapshots[0]), snapshots)
    insert('source_record', ('case_id','snapshot_id','business_key','entity_id','period_id','component','segment_id','amount','record_status','changed_from_previous','duplicate_group_id','included_by_filter','source_table','source_column'), c['source_records'])
    insert('semantic_change_evidence', ('case_id','semantic_type','previous_id','current_id','previous_hash','current_hash','affected_population_count','estimated_impact','details_json'), [dict(x,case_id='CASE_0042',details_json=None) for x in c['semantic_evidence']])
    insert('pipeline_run_evidence', ('case_id','pipeline_run_id','run_ts','source_snapshot_id','execution_status','replay_of_run_id','rows_written','duplicate_rows_written','note'), [dict(x,case_id='CASE_0042',note=None) for x in c['pipeline_evidence']])
    insert('technical_lineage_curated', ('case_id','source_table','source_column','target_table','target_column','entity_type','event_time','lineage_source'), [dict(x,case_id='CASE_0042',event_time=None) for x in c['technical_lineage']])
    return '\n'.join(statements)+'\n'

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--target',default='local'); ap.add_argument('--case',default='CASE_0042'); ap.add_argument('--plan',action='store_true'); ap.add_argument('--apply',action='store_true'); ap.add_argument('--verify',action='store_true'); ap.add_argument('--profile',default=os.getenv('DATABRICKS_CONFIG_PROFILE','')); ap.add_argument('--warehouse-id',default=os.getenv('MDL_WAREHOUSE_ID','')); ap.add_argument('--manifest',default='release-report/MDL-2/seed-manifest.json'); ap.add_argument('--sql-out',default='release-report/MDL-2/seed-case-0042.sql'); a=ap.parse_args()
    if a.case != 'CASE_0042': raise SystemExit('only CASE_0042 is in the locked MDL-2 seed scope')
    if a.target not in ('local','staging') or (a.apply and a.target!='staging') or (a.verify and a.target!='staging'): raise SystemExit('target/apply/verify combination is not permitted')
    if a.apply and a.plan: raise SystemExit('--plan and --apply are mutually exclusive')
    case=generate_case(a.case); catalog=os.getenv('MDL_CATALOG','{{MDL_CATALOG}}'); sql=migration(catalog,case)
    out=ROOT/a.sql_out; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(sql,encoding='utf-8')
    payload={'mode':'apply' if a.apply else ('verify' if a.verify else 'plan'),'target':a.target,'case_id':a.case,'canonical_case_hash':case.content_hash,'sql_path':a.sql_out,'private_truth_included':False}
    if a.apply or a.verify:
        if catalog.startswith('{{'): raise SystemExit('staging apply requires MDL_CATALOG')
        try:
            if a.profile:
                if not a.warehouse_id: raise SystemExit('--warehouse-id or MDL_WAREHOUSE_ID is required with --profile')
                from databricks.sdk import WorkspaceClient
                from scripts.live_sql_check import SdkConnection
                connection = SdkConnection(WorkspaceClient(profile=a.profile), a.warehouse_id)
            else:
                connection = connect_from_env()
            with connection:
                with connection.cursor() as cursor:
                    if a.apply:
                        for statement in sql.splitlines():
                            if statement.strip(): execute_native(cursor,statement,())
                    execute_native(cursor, f"SELECT case_id FROM {catalog}.mad_data_lab_public.case_definition WHERE case_id = ?", (a.case,))
        except SqlAdapterError as exc: raise SystemExit(f'seed: NOT RUN ({exc})') from exc
    manifest=ROOT/a.manifest; manifest.parent.mkdir(parents=True,exist_ok=True); manifest.write_text(json.dumps(payload,sort_keys=True,indent=2),encoding='utf-8'); print(json.dumps(payload,sort_keys=True))
if __name__=='__main__': main()
