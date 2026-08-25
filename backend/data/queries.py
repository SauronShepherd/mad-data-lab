from dataclasses import dataclass

@dataclass(frozen=True)
class QuerySpec:
    query_id: str
    sql_path: str
    result_model: str
    parameter_names: tuple[str, ...] = ("case_id",)

QUERIES={f'Q{i}': QuerySpec(f'Q{i}', name, model, ("case_id", "limit") if i == 4 else ("case_id",)) for i,(name,model) in enumerate([
 ('observation.sql','Observation'),('component_decomposition.sql','Component'),('snapshot_summary.sql','Snapshot'),('highest_impact_records.sql','SourceRecord'),('dq_materiality.sql','Quality'),('formula_validation.sql','Formula'),('value_lineage.sql','Lineage'),('reconciliation.sql','Reconciliation')],1)}

def get_query(query_id):
    try: return QUERIES[query_id]
    except KeyError: raise ValueError('unsupported query id')
