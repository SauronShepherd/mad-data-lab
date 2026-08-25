"""Fail-closed repository audit for the implementable MDL-2 contract."""
from __future__ import annotations
import argparse, json, re, sys, subprocess
from pathlib import Path

_SCRIPT_PATH = globals().get('__file__') or (sys.argv[0] if sys.argv else '')
ROOT=Path(_SCRIPT_PATH).resolve().parents[1]
def current_identity():
    head=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True).stdout.strip() or 'NOT_IN_GIT'
    runtime=subprocess.check_output([sys.executable,'scripts/compute_runtime_digest.py'],cwd=ROOT,text=True).strip()
    data=subprocess.check_output([sys.executable,'scripts/compute_mdl2_data_digest.py'],cwd=ROOT,text=True).strip()
    return {'git_head':head,'runtime_digest':runtime,'data_contract_digest':data}
REQUIRED=('cases/templates/case_0042.yaml','cases/completion_contracts/case_0042_v1.yaml','cases/schemas/case_template.schema.json','cases/schemas/completion_contract.schema.json','data/generation/generator.py','data/generation/mutations.py','data/generation/private_specs/case_0042_v1.yaml','data/fixtures/public/case_0042.bundle.json','data/fixtures/private/case_0042_truth.json','backend/data/repositories.py','backend/data/sql_client.py','scripts/seed_databricks.py','scripts/apply_databricks_schema.py','scripts/snapshot_case_data.py','scripts/restore_case_data.py','scripts/verify_databricks_data.py','scripts/mdl2_property_suite.py','scripts/mdl2_sql_preflight.py','docs/traceability/MDL-2-predecessor.json','docs/traceability/v3-test-coverage.csv','docs/approvals/MDL-2-art.md','assets/review/MDL-2/art-generation-plan.json','databricks.yml','resources/mdl2.yml','uv.lock')
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--strict',action='store_true'); a=ap.parse_args(); checks=[]
    for rel in REQUIRED: checks.append((f'path:{rel}',(ROOT/rel).is_file()))
    public=(ROOT/'data/fixtures/public').read_text(encoding='utf-8',errors='ignore') if False else '\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in (ROOT/'data/fixtures/public').glob('*.json'))
    for marker in ('truth_json','primary_cause','expected_path_json','allowed_final_status_json'): checks.append((f'public-excludes:{marker}',marker not in public))
    for path in (ROOT/'sql/trusted').glob('*.sql'):
        text=path.read_text(encoding='utf-8'); checks.extend([(f'{path.name}:native-params',':case_id' not in text and ':limit' not in text),(f'{path.name}:no-private', 'mad_data_lab_private' not in text)])
    art=json.loads((ROOT/'release-report/MDL-2/art-preflight.json').read_text(encoding='utf-8')); checks.append(('art-preflight',art.get('status')=='CANDIDATES_PREFLIGHT_PASS'))
    identity=current_identity()
    for name in ('genie-eval.json','deployed-smoke.json','deployed-soak.json'):
        payload=json.loads((ROOT/'release-report'/name).read_text(encoding='utf-8')); checks.append((f'live-evidence:{name}',payload.get('status')=='PASS'))
        recorded=payload.get('source_identity',{})
        checks.append((f'live-evidence-current:{name}', all(recorded.get(key)==value for key,value in identity.items())))
    for rel in ('release-report/MDL-2/golden-case.json','release-report/MDL-2/generator.json','release-report/MDL-2/privacy-static.json','release-report/MDL-2/schema-fingerprint.json','release-report/MDL-2/data-contract-digest.json','release-report/MDL-2/iteration-gate.json','docs/traceability/mdl2-data-contract.json'):
        checks.append((f'closure-artifact:{rel}',(ROOT/rel).is_file()))
    expected_digest=subprocess.check_output([sys.executable,'scripts/compute_mdl2_data_digest.py'],cwd=ROOT,text=True).strip()
    digest_payload=json.loads((ROOT/'release-report/MDL-2/data-contract-digest.json').read_text(encoding='utf-8'))
    checks.append(('data-digest-current',digest_payload.get('sha256')==expected_digest))
    canonical_hash=(ROOT/'data/fixtures/hashes/case_0042.sha256').read_text(encoding='utf-8').strip()
    golden=json.loads((ROOT/'release-report/MDL-2/golden-case.json').read_text(encoding='utf-8'))
    checks.append(('canonical-hash-current',golden.get('sha256')==canonical_hash))
    failed=[name for name,ok in checks if not ok]
    sql_evidence=ROOT/'release-report/MDL-2/sql-integration.json'
    pending=['human-art-approval','predecessor-mdl1']
    v3_record=ROOT/'docs/traceability/v3-source.json'
    if not v3_record.is_file() or json.loads(v3_record.read_text(encoding='utf-8')).get('status') != 'VERIFIED':
        pending.append('accepted-v3-source')
    if not sql_evidence.is_file() or json.loads(sql_evidence.read_text(encoding='utf-8')).get('status') != 'PASS': pending.insert(1,'live-databricks-sql')
    predecessor=(ROOT/'docs/iterations/MDL-1-entry.md').read_text(encoding='utf-8')
    checks.append(('predecessor-record-explicit', 'BLOCKED_PREDECESSOR_EVIDENCE_NOT_PROVABLE' in predecessor))
    report=(ROOT/'docs/iterations/MDL-2-report.md').read_text(encoding='utf-8')
    checks.append(('report-not-falsely-complete', 'status: COMPLETE' not in report or all(x not in report for x in ('NOT_RUN','PENDING','BLOCKED'))))
    result={'status':'PASS' if not failed and not (a.strict and pending) else 'IN_PROGRESS','checks':len(checks),'failed':failed,'pending':pending}
    out=ROOT/'release-report/MDL-2/contract-validation.json'; out.write_text(json.dumps(result,indent=2,sort_keys=True),encoding='utf-8'); print(json.dumps(result,indent=2));
    if failed or (a.strict and pending): raise SystemExit(1)
if __name__=='__main__': main()
