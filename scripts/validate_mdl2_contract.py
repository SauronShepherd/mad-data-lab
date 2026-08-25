"""Fail-closed repository audit for the implementable MDL-2 contract."""
from __future__ import annotations
import argparse, json, sys, subprocess
from pathlib import Path

_SCRIPT_PATH = globals().get('__file__') or (sys.argv[0] if sys.argv else '')
ROOT=Path(_SCRIPT_PATH).resolve().parents[1]
def current_identity():
    # Evidence must bind to the actual checked-out tree.  The iteration report
    # is descriptive metadata and may intentionally lag a later remediation;
    # it must never override git HEAD for release identity.
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
    art_approval=ROOT/'docs/approvals/MDL-2-art-approval.json'
    art_approved=False
    if art_approval.is_file():
        approval=json.loads(art_approval.read_text(encoding='utf-8'))
        art_approved=approval.get('status')=='APPROVED' and bool(approval.get('human_reviewer'))
        for asset_id, selection in approval.get('selected_exact_byte_hashes', {}).items():
            path=ROOT/selection.get('path','')
            actual=__import__('hashlib').sha256(path.read_bytes()).hexdigest() if path.is_file() else ''
            checks.append((f'art-approval-hash:{asset_id}',actual==selection.get('sha256')))
    checks.append(('art-approval-record', not art_approval.exists() or art_approved))
    identity=current_identity()
    live_refresh_pending=[]
    for name in ('genie-eval.json','deployed-smoke.json','deployed-soak.json'):
        payload=json.loads((ROOT/'release-report'/name).read_text(encoding='utf-8'))
        live_pass=payload.get('status')=='PASS'
        checks.append((f'live-evidence:{name}',live_pass))
        if not live_pass:
            live_refresh_pending.append(f'live-evidence-refresh:{name}')
        recorded=payload.get('source_identity',{})
        current=all(recorded.get(key)==value for key,value in identity.items())
        if not current:
            # Historical PASS evidence must never certify a new runtime.  In
            # normal mode this is an explicit refresh obligation so the
            # validator can describe an honest IN_PROGRESS repository; strict
            # release validation promotes it to a hard failure below.
            live_refresh_pending.append(f'live-evidence-refresh:{name}')
        checks.append((f'live-evidence-current:{name}', current))
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
    pending=['predecessor-mdl1', *live_refresh_pending]
    if not art_approved:
        pending.insert(0,'human-art-approval')
    v3_record=ROOT/'docs/traceability/v3-source.json'
    if not v3_record.is_file() or json.loads(v3_record.read_text(encoding='utf-8')).get('status') != 'VERIFIED':
        pending.append('accepted-v3-source')
    if not sql_evidence.is_file() or json.loads(sql_evidence.read_text(encoding='utf-8')).get('status') != 'PASS': pending.insert(1,'live-databricks-sql')
    predecessor=(ROOT/'docs/iterations/MDL-1-entry.md').read_text(encoding='utf-8')
    checks.append(('predecessor-record-explicit', 'BLOCKED_PREDECESSOR_EVIDENCE_NOT_PROVABLE' in predecessor))
    report=(ROOT/'docs/iterations/MDL-2-report.md').read_text(encoding='utf-8')
    checks.append(('report-not-falsely-complete', 'status: COMPLETE' not in report or all(x not in report for x in ('NOT_RUN','PENDING','BLOCKED'))))
    if not a.strict:
        failed=[name for name in failed if not name.startswith('live-evidence')]
    pending=list(dict.fromkeys(pending))
    result={'status':'PASS' if not failed and not pending else 'IN_PROGRESS','checks':len(checks),'failed':failed,'pending':pending,'diagnostics':{'current_identity':identity,'expected_data_digest':expected_digest,'recorded_data_digest':digest_payload.get('sha256')}}
    out=ROOT/'release-report/MDL-2/contract-validation.json'; out.write_text(json.dumps(result,indent=2,sort_keys=True),encoding='utf-8'); print(json.dumps(result,indent=2));
    if failed or (a.strict and pending): raise SystemExit(1)
if __name__=='__main__': main()
