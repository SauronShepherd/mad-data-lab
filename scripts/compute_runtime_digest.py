"""Hash runtime-affecting source and built application content."""
import hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PREFIXES=('server','backend','data','cases','genie','src','index.html','package.json','package-lock.json','pyproject.toml','uv.lock','Dockerfile','app.yaml','databricks.yml','resources')
def files():
    result=[]
    for name in PREFIXES:
        p=ROOT/name
        if p.is_file(): result.append(p)
        elif p.is_dir(): result.extend(x for x in p.rglob('*') if x.is_file() and '__pycache__' not in x.parts)
    return sorted(set(result), key=lambda p:p.relative_to(ROOT).as_posix())
def digest():
    h=hashlib.sha256()
    for p in files():
        raw = p.read_bytes()
        try:
            # Git checkouts may use CRLF on Windows and LF on Linux. Runtime
            # identity must bind semantic source content, not checkout style.
            content = raw.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n').encode('utf-8')
        except UnicodeDecodeError:
            content = raw
        h.update(p.relative_to(ROOT).as_posix().encode()+b'\0'+content+b'\0')
    return h.hexdigest()
if __name__=='__main__': print(digest())
