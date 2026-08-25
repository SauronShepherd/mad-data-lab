from decimal import Decimal
import hashlib, json
from pathlib import Path
from functools import lru_cache
import yaml
from .canonical import canonical_hash, money, population_hash
from .models import GeneratedCase
from .stable_rng import StableRng
from .validators import validate_case

FORMULA = 'V1 + V2 - V3 + V4'
FORMULA_HASH = hashlib.sha256(FORMULA.encode()).hexdigest()
PHASES = ('LOAD_TEMPLATE','VALIDATE_TEMPLATE','LOAD_PRIVATE_SPEC','RESOLVE_VERSIONS_AND_SEED','BUILD_BASELINE_RECORDS','COMPUTE_PREVIOUS_METRIC','APPLY_PRIMARY_MUTATION','APPLY_SECONDARY_SIGNAL','MATERIALIZE_CURRENT_RECORDS','COMPUTE_CURRENT_METRIC','BUILD_SNAPSHOT_DIFF','BUILD_DQ_EVIDENCE','BUILD_SEMANTIC_EVIDENCE','BUILD_CALCULATION_LINEAGE','BUILD_TECHNICAL_LINEAGE_FALLBACK','BUILD_PRIVATE_TRUTH','VALIDATE_GLOBAL_INVARIANTS','VALIDATE_CASE_0042_INVARIANTS','CANONICALIZE','HASH','PERSIST_FIXTURES')

_ROOT = Path(__file__).resolve().parents[2]

@lru_cache(maxsize=1)
def _load_contracts():
    template = yaml.safe_load((_ROOT / 'cases/templates/case_0042.yaml').read_text(encoding='utf-8'))
    private_spec = yaml.safe_load((_ROOT / 'data/generation/private_specs/case_0042_v1.yaml').read_text(encoding='utf-8'))
    if template.get('case_id') != 'CASE_0042' or private_spec.get('case_id') != 'CASE_0042':
        raise ValueError('Case #042 contract identifiers do not agree')
    if template.get('generator_version') != private_spec.get('generator_version'):
        raise ValueError('Case #042 generator versions do not agree')
    return template, private_spec

def _rows():
    rows=[]
    groups=[('TX-004291', '4.20','0.00'), *[(f'TX-{i:06d}', '0.50','0.44') for i in range(4292,4297)], *[(f'TX-{i:06d}','0.50','0.46') for i in range(4297,4312)], *[(f'TX-{i:06d}','0.50','0.45') for i in range(4312,4314)]]
    for key, old, new in groups: rows.append({'business_key':key,'component':'V2','old_value':old,'new_value':new,'impact':str(money(new)-money(old)),'change_type':'MODIFIED'})
    rows += [{'business_key':'TX-004314','component':'V2','old_value':'0.50','new_value':None,'impact':'-0.50','change_type':'REMOVED'},{'business_key':'TX-004315','component':'V2','old_value':'0.30','new_value':None,'impact':'-0.30','change_type':'REMOVED'}]
    rows += [{'business_key':f'TX-{i:06d}','component':'V2','old_value':None,'new_value':'0.02','impact':'0.02','change_type':'ADDED'} for i in range(4316,4321)]
    rows += [{'business_key':f'TX-{i:06d}','component':'V2','old_value':'1.00','new_value':'1.00','impact':'0.00','change_type':'UNCHANGED'} for i in range(4321,4335)]
    return rows

def generate_case(case_template_id='case_0042', seed=None, generator_version=None, *, mode='release'):
    if case_template_id not in ('case_0042','CASE_0042'): raise ValueError('unsupported case template')
    if mode=='release' and seed not in (None,42): raise ValueError('release Case #042 seed is fixed at 42')
    template, private_spec = _load_contracts()
    gv = template['generator_version'] if generator_version is None else generator_version
    if gv != template['generator_version']:
        raise ValueError('unsupported Case #042 generator version')
    resolved_seed = 42 if seed is None else seed
    # Every generated case resolves its decisions through the stable, namespaced
    # RNG.  Release values are locked, while property runs can use the same
    # deterministic decision stream without changing the release artifact.
    rng = StableRng('CASE_0042', template['case_template_version'], gv, resolved_seed)
    _ = rng.bytes('mutation-plan')
    rows=_rows(); components=[{'component':k,'previous_value':a,'current_value':b,'contribution_delta':d} for k,a,b,d in [('V1','100.10','98.90','-1.20'),('V2','30.00','24.10','-5.90'),('V3','5.10','4.80','0.30'),('V4','0.00','0.00','0.00')]]
    diffs=[r for r in rows if r['change_type']!='UNCHANGED']; changed_keys=[r['business_key'] for r in rows if r['change_type']=='MODIFIED' and r['business_key']!='TX-004291'][:5]
    public={'case_id':'CASE_0042','public_number':42,'title':'The Missing €6.8M','expected_value':'125.00','observed_value':'118.20','deviation':'-6.80','generator_version':gv,'case_template_version':1,'formula_id':'CAPITAL_AVAILABLE_V1','formula_hash':FORMULA_HASH,'filter_id':'CAPITAL_AVAILABLE_FILTER_V1','filter_hash':hashlib.sha256(b'CAPITAL_AVAILABLE_FILTER_V1').hexdigest(),'created_at':'2026-08-03T09:00:00Z','component_evidence':components,'snapshot_evidence':diffs,'quality_evidence':[{'issue_id':'DQ_0042_01','rule_name':'DUPLICATE_BUSINESS_KEY','affected_keys':changed_keys,'affected_row_count':5,'estimated_impact':'-0.30','impact_is_overlapping':True}],'source_snapshots':[{'snapshot_id':'SNAP_20260802_0900','row_count':42,'role':'PREVIOUS','run_id':'RUN_0042_20260802_0900','run_ts':'2026-08-02T09:00:00Z','population_hash':''},{'snapshot_id':'SNAP_20260803_0900','row_count':45,'role':'CURRENT','run_id':'RUN_0042_20260803_0900','run_ts':'2026-08-03T09:00:00Z','population_hash':''}],'semantic_evidence':[{'semantic_type':'FORMULA','previous_id':'CAPITAL_AVAILABLE_V1','current_id':'CAPITAL_AVAILABLE_V1','previous_hash':FORMULA_HASH,'current_hash':FORMULA_HASH,'changed':False,'affected_population_count':0,'estimated_impact':'0.00'}],'pipeline_evidence':[{'pipeline_run_id':'RUN_0042_20260802_0900','run_ts':'2026-08-02T09:00:00Z','source_snapshot_id':'SNAP_20260802_0900','execution_status':'SUCCESS','replay_of_run_id':None,'rows_written':42,'duplicate_rows_written':0},{'pipeline_run_id':'RUN_0042_20260803_0900','run_ts':'2026-08-03T09:00:00Z','source_snapshot_id':'SNAP_20260803_0900','execution_status':'SUCCESS','replay_of_run_id':None,'rows_written':45,'duplicate_rows_written':0}],'value_lineage':[{'node_id':'CAPITAL_AVAILABLE','node_type':'METRIC','parent_node_id':None,'sequence_no':0},{'node_id':'V2','node_type':'COMPONENT','parent_node_id':'CAPITAL_AVAILABLE','sequence_no':1},{'node_id':'finance_reporting_source.amount','node_type':'SOURCE_COLUMN','parent_node_id':'V2','sequence_no':2}],'technical_lineage':[{'source_table':'finance_reporting_source','source_column':'amount','target_table':'datapoint_result','target_column':'value','entity_type':'COLUMN','lineage_source':'TECHNICAL_LINEAGE_FALLBACK'}]}
    if mode == 'property_test':
        public['property_seed'] = 42 if seed is None else seed
        public['property_template'] = 'level1_clean' if resolved_seed % 2 == 0 else 'level2_noisy'
        public['property_signature'] = rng.bytes('property-signature').hex()
    truth = private_spec['expected_truth']
    private={'case_id':'CASE_0042','primary_component':truth['primary_component'],'primary_cause':truth['primary_cause'],'secondary_cause':truth['secondary_cause'],'expected_total_deviation':truth['expected_total_deviation'],'truth_json':'private'}
    # The canonical public package is intentionally safe to ship.  The oracle is
    # returned separately for release validation and is never part of its hash.
    # The public package is a named-domain document.  Keeping these domains
    # explicit prevents a later SQL seed/view from silently inventing a second
    # shape for the same Case.
    source_records=[]
    for role, snapshot_id, values_key in (
        ('PREVIOUS', 'SNAP_20260802_0900', 'old_value'),
        ('CURRENT', 'SNAP_20260803_0900', 'new_value'),
    ):
        for row in rows:
            value = row[values_key]
            if value is None:
                continue
            source_records.append({
                'case_id':'CASE_0042', 'snapshot_id':snapshot_id,
                'business_key':row['business_key'], 'component':row['component'],
                'amount':value, 'entity_id':'PT001', 'period_id':'2026-07',
                'segment_id':None, 'record_status':'ACTIVE',
                'changed_from_previous': role == 'CURRENT' and row['change_type'] in ('MODIFIED','ADDED'),
                'included_by_filter':True, 'duplicate_group_id':None,
                'source_table':'finance_reporting_source', 'source_column':'amount',
            })
        for component, old_value, new_value in (('V1','100.10','98.90'),('V3','5.10','4.80'),('V4','0.00','0.00')):
            value = old_value if role == 'PREVIOUS' else new_value
            source_records.append({'case_id':'CASE_0042','snapshot_id':snapshot_id,'business_key':f'{component}-BASE-001','component':component,'amount':value,'entity_id':'PT001','period_id':'2026-07','segment_id':None,'record_status':'ACTIVE','changed_from_previous':role == 'CURRENT' and component != 'V4','included_by_filter':True,'duplicate_group_id':None,'source_table':'finance_reporting_source','source_column':'amount'})
    public['source_snapshots'][0]['population_hash']=population_hash([r for r in source_records if r['snapshot_id']=='SNAP_20260802_0900' and r['included_by_filter']])
    public['source_snapshots'][1]['population_hash']=population_hash([r for r in source_records if r['snapshot_id']=='SNAP_20260803_0900' and r['included_by_filter']])
    canonical={
        'schema_version':'MDL-2.case-package.v1',
        'case_definition':{k:v for k,v in public.items() if k not in {'component_evidence','snapshot_evidence','quality_evidence','source_snapshots','semantic_evidence','pipeline_evidence','value_lineage','technical_lineage'}},
        'datapoint_results':[{'case_id':'CASE_0042','datapoint_id':'CAPITAL_AVAILABLE','run_role':role,'run_id':item['run_id'],'run_ts':item['run_ts'],'expected_value':public['expected_value'],'observed_value':public['observed_value'],'deviation':public['deviation'],'formula_id':public['formula_id'],'formula_hash':public['formula_hash'],'population_hash':item['population_hash']} for role,item in (('PREVIOUS',public['source_snapshots'][0]),('CURRENT',public['source_snapshots'][1]))],
        'calculation_trace':public['value_lineage'],
        'source_snapshots':public['source_snapshots'],
        'source_records':source_records,
        'snapshot_diff':public['snapshot_evidence'],
        'quality_issues':public['quality_evidence'],
        'semantic_evidence':public['semantic_evidence'],
        'pipeline_evidence':public['pipeline_evidence'],
        'technical_lineage':public['technical_lineage'],
        'curated_expected_outputs':{'component_evidence':public['component_evidence']},
    }
    validate_case(public)
    return GeneratedCase(public, private, canonical, canonical_hash(canonical), PHASES)
