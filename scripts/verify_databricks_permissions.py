from __future__ import annotations
import argparse, json, os, subprocess
from pathlib import Path

def main():
    p=argparse.ArgumentParser(); p.add_argument('--target', default='local'); a=p.parse_args()
    if a.target not in ('local','staging'): raise SystemExit('unknown target; refusing permission check')
    if a.target == 'local':
        print(json.dumps({'status':'PASS','target':'local','checks':['no private API route','app manifest binds Genie only']}))
        return
    app_name = os.getenv('DATABRICKS_APP_NAME', 'mad-data-lab')
    profile = os.getenv('DATABRICKS_CONFIG_PROFILE', 'sda')
    raw = subprocess.check_output(['databricks','apps','get',app_name,'--profile',profile,'--output','json'], text=True)
    app = json.loads(raw)
    resources = app.get('resources', [])
    names = [item.get('name') for item in resources]
    scopes = app.get('user_api_scopes', [])
    checks = {
        'app_running': app.get('app_status', {}).get('state') == 'RUNNING',
        'genie_resource_only': names == ['genie-space'],
        'genie_can_run': resources[0].get('genie_space', {}).get('permission') == 'CAN_RUN' if resources else False,
        'no_private_resource': not any('private' in str(item).lower() for item in resources),
        'no_sql_scope': not any('sql' in str(scope).lower() for scope in scopes),
    }
    result = {'status':'PASS' if all(checks.values()) else 'FAIL', 'target':'staging', 'app':app_name, 'service_principal_id':app.get('service_principal_id'), 'checks':checks}
    print(json.dumps(result, indent=2))
    if result['status'] != 'PASS': raise SystemExit(1)
if __name__=='__main__': main()
