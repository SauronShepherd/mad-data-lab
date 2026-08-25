"""Compile/check the MDL-2 SQL source tree without contacting Databricks."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
import re
import sys
_SCRIPT_PATH = globals().get('__file__') or (sys.argv[0] if sys.argv else '')
ROOT = Path(_SCRIPT_PATH).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from backend.data.queries import QUERIES

def main() -> None:
    ddl = sorted((ROOT / 'data/ddl').glob('*.sql'))
    views = sorted((ROOT / 'data/views').glob('*.sql'))
    trusted = sorted((ROOT / 'sql/trusted').glob('*.sql'))
    assert len(ddl) >= 11, f'expected complete DDL set, found {len(ddl)}'
    assert len(views) == 8, f'expected 8 curated views, found {len(views)}'
    assert len(trusted) == 8, f'expected Q1-Q8 trusted SQL, found {len(trusted)}'
    expected_paths = {spec.sql_path: spec for spec in QUERIES.values()}
    assert set(expected_paths) == {path.name for path in trusted}, 'trusted SQL and query registry are out of sync'
    digest = hashlib.sha256()
    for path in [*ddl, *views, *trusted]:
        text = path.read_text(encoding='utf-8')
        assert ':case_id' not in text and ':limit' not in text, f'named parameter in {path.name}'
        if path in trusted:
            spec = expected_paths[path.name]
            assert len(re.findall(r'\?', text)) == len(spec.parameter_names), f'parameter metadata mismatch in {path.name}'
        if path in trusted:
            assert 'mad_data_lab_private' not in text, f'private object in {path.name}'
        digest.update(path.relative_to(ROOT).as_posix().encode() + b'\0' + path.read_bytes() + b'\0')
    payload = {'status':'PASS','ddl_files':len(ddl),'view_files':len(views),'trusted_queries':len(trusted),'sql_source_digest':digest.hexdigest()}
    out = ROOT / 'release-report/MDL-2/sql-preflight.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding='utf-8')
    print(json.dumps(payload, sort_keys=True))

if __name__ == '__main__': main()
