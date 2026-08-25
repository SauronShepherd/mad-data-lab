from decimal import Decimal
from .canonical import money

def validate_case(case):
    p = case; comps = case['component_evidence']; diffs = case['snapshot_evidence']
    assert money(p['observed_value']) - money(p['expected_value']) == money('-6.80')
    assert sum((money(x['contribution_delta']) for x in comps), Decimal()) == money('-6.80')
    v2 = [x for x in diffs if x['component'] == 'V2']
    assert sum((money(x['impact']) for x in v2), Decimal()) == money('-5.90')
    assert len([x for x in v2 if x['change_type']=='MODIFIED']) == 23
    assert len([x for x in v2 if x['change_type']=='REMOVED']) == 2
    assert len([x for x in v2 if x['change_type']=='ADDED']) == 5
    tx = next(x for x in v2 if x['business_key']=='TX-004291')
    assert money(tx['impact']) == money('-4.20')
    q = case['quality_evidence'][0]
    assert q['affected_row_count'] == 5 and q['impact_is_overlapping'] is True
    assert money(q['estimated_impact']) == money('-0.30')
    return True
