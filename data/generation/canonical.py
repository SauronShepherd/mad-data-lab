import hashlib, json
import unicodedata
from decimal import Decimal, ROUND_HALF_UP

def _default(value):
    if isinstance(value, Decimal): return format(value, '.2f')
    raise TypeError(type(value).__name__)

def canonical_bytes(value):
    sort_keys = {
        'datapoint_results': ('case_id','run_ts','run_id'),
        'calculation_trace': ('case_id','sequence_no','node_id'),
        'source_snapshots': ('case_id','run_ts','snapshot_id'),
        'source_records': ('case_id','snapshot_id','component','business_key'),
        'snapshot_diff': ('case_id','component','business_key','change_type'),
        'quality_issues': ('case_id','issue_id'),
        'semantic_evidence': ('case_id','semantic_type','previous_id','current_id'),
        'pipeline_evidence': ('case_id','run_ts','pipeline_run_id'),
        'technical_lineage': ('case_id','source_table','source_column','target_table','target_column'),
    }
    def normalize(item, parent_key=None):
        if isinstance(item, str): return unicodedata.normalize('NFC', item)
        if isinstance(item, dict): return {k: normalize(v, k) for k, v in item.items()}
        if isinstance(item, list):
            normalized = [normalize(v, parent_key) for v in item]
            fields = sort_keys.get(parent_key or '')
            if fields and all(isinstance(v, dict) for v in normalized):
                normalized.sort(key=lambda row: tuple('' if row.get(field) is None else str(row.get(field)) for field in fields))
            return normalized
        return item
    return json.dumps(normalize(value), ensure_ascii=False, sort_keys=True, separators=(',', ':'), default=_default).encode()

def canonical_hash(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()

def money(value):
    return Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def population_hash(records):
    """Stable MDL-2 population hash; independent of SQL/Spark row order."""
    fields = ('business_key','component','amount','entity_id','period_id','record_status','changed_from_previous','included_by_filter','duplicate_group_id','source_table','source_column')
    rows=[]
    for row in sorted(records, key=lambda r: (r['component'], r['business_key'])):
        values=[]
        for field in fields:
            value=row.get(field)
            if value is None: value=''
            elif isinstance(value, bool): value='true' if value else 'false'
            elif field == 'amount': value=f"{money(value):.2f}"
            values.append(str(value))
        rows.append('|'.join(values))
    return hashlib.sha256('\n'.join(rows).encode('utf-8')).hexdigest()
