from __future__ import annotations
import argparse, hashlib
from pathlib import Path

def main():
    p=argparse.ArgumentParser(); p.add_argument('--source-root', default='data'); a=p.parse_args()
    root=Path(a.source_root); h=hashlib.sha256()
    files=sorted(x for x in root.rglob('*.sql') if x.is_file())
    for f in files: h.update(f.as_posix().encode()+b'\0'+f.read_bytes()+b'\0')
    print({'source_sql_files':len(files),'source_sql_digest':h.hexdigest()})
if __name__=='__main__': main()
