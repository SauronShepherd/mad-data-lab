"""Hash runtime-affecting source and built application content."""
import hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PREFIXES=('server','backend','data','src','index.html','package.json','package-lock.json','pyproject.toml','uv.lock','requirements.txt','Dockerfile','app.yaml','databricks.yml','resources')
def files():
    result=[]
    for name in PREFIXES:
        p=ROOT/name
        if p.is_file(): result.append(p)
        elif p.is_dir(): result.extend(x for x in p.rglob('*') if x.is_file() and '__pycache__' not in x.parts)
    return sorted(set(result), key=lambda p:p.relative_to(ROOT).as_posix())
def digest():
    h=hashlib.sha256()
    for p in files(): h.update(p.relative_to(ROOT).as_posix().encode()+b'\0'+p.read_bytes()+b'\0')
    return h.hexdigest()
if __name__=='__main__': print(digest())
