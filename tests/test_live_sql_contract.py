import subprocess,sys
from pathlib import Path
def test_live_sql_plan_uses_all_closed_queries_and_no_legacy_schema():
    root=Path(__file__).parents[1]
    result=subprocess.run([sys.executable,'scripts/live_sql_check.py','--plan'],cwd=root,capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    assert set(__import__('json').loads(result.stdout)['queries']) == {f'Q{i}' for i in range(1,9)}
    assert 'sda_dev.mad_data_lab' not in result.stdout

def test_q4_declares_and_binds_case_and_limit_parameters():
    from backend.data.queries import QUERIES
    assert QUERIES['Q4'].parameter_names == ('case_id', 'limit')
    assert QUERIES['Q1'].parameter_names == ('case_id',)

def test_query_registry_matches_trusted_sql_placeholder_counts():
    import re
    from pathlib import Path
    from backend.data.queries import QUERIES
    for spec in QUERIES.values():
        sql = (Path(__file__).parents[1] / 'sql' / 'trusted' / spec.sql_path).read_text(encoding='utf-8')
        assert len(re.findall(r'\?', sql)) == len(spec.parameter_names)
