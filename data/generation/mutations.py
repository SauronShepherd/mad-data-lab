from dataclasses import dataclass

OPERATORS = ('VALUE_CHANGE','MISSING_ROWS','NEW_ROWS','DUPLICATE_KEYS','PIPELINE_REPLAY','FORMULA_CHANGE','FILTER_CHANGE','ENTITY_MIX','JOIN_CARDINALITY','MULTI_CAUSE')
@dataclass(frozen=True)
class MutationResult:
    operator_id: str
    records: tuple
    evidence: dict

def apply_operator(operator_id, records, *, changed=None):
    if operator_id not in OPERATORS: raise ValueError(f'unknown mutation operator: {operator_id}')
    copied = tuple(dict(r) for r in records)
    if operator_id == 'VALUE_CHANGE' and changed:
        for row in copied:
            if row['business_key'] == changed['business_key']: row['amount'] = changed['amount']
    elif operator_id == 'MISSING_ROWS':
        copied = tuple(row for row in copied if not row.get('remove'))
    elif operator_id == 'NEW_ROWS' and changed:
        copied = copied + (dict(changed),)
    elif operator_id == 'DUPLICATE_KEYS' and copied:
        copied = copied + (dict(copied[0]) | {'duplicate_group_id': 'TEST_DUPLICATE'},)
    elif operator_id == 'PIPELINE_REPLAY':
        copied = tuple(dict(row) | {'replay_of_run_id': row.get('run_id')} for row in copied)
    elif operator_id == 'FORMULA_CHANGE':
        copied = tuple(dict(row) | {'formula_changed': True} for row in copied)
    elif operator_id == 'FILTER_CHANGE':
        copied = tuple(dict(row) | {'included_by_filter': not row.get('included_by_filter', True)} for row in copied)
    elif operator_id == 'ENTITY_MIX':
        copied = tuple(dict(row) | {'entity_id': row.get('entity_id', 'ENTITY_A')} for row in copied)
    elif operator_id == 'JOIN_CARDINALITY':
        copied = tuple(dict(row) | {'join_multiplicity': 2} for row in copied)
    elif operator_id == 'MULTI_CAUSE':
        copied = tuple(dict(row) | {'causal_role': 'PRIMARY_OR_SECONDARY'} for row in copied)
    return MutationResult(operator_id, copied, {'operator_id': operator_id, 'affected_count': len(copied), 'pure': True})
