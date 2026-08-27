import hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PREFIXES=('cases/templates','cases/completion_contracts','data/ddl','data/views','data/generation','data/validation','sql/trusted','backend/data','scripts/generate_cases.py','scripts/validate_cases.py','scripts/seed_databricks.py','scripts/snapshot_case_data.py','scripts/restore_case_data.py','scripts/verify_databricks_data.py','scripts/fingerprint_databricks_objects.py','scripts/verify_databricks_permissions.py','pyproject.toml','uv.lock','databricks.yml','resources/mdl2.yml')
def paths():
    out=[]
    for prefix in PREFIXES:
        p=ROOT/prefix
        if p.is_file(): out.append(p)
        elif p.is_dir(): out.extend(x for x in p.rglob('*') if x.is_file() and '__pycache__' not in x.parts and x.suffix != '.pyc')
    return sorted(set(out), key=lambda p:p.relative_to(ROOT).as_posix())
def digest():
    h=hashlib.sha256()
    for p in paths():
        raw = p.read_bytes()
        try:
            # Keep the contract identity stable across Windows/Linux checkout
            # line-ending normalization, just like the runtime digest.
            content = raw.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n').encode('utf-8')
        except UnicodeDecodeError:
            content = raw
        h.update(p.relative_to(ROOT).as_posix().encode()); h.update(b'\0'); h.update(content); h.update(b'\0')
    return h.hexdigest()
if __name__=='__main__': print(digest())
