"""Compute the MDL-4 gameplay contract digest from runtime-relevant files."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = ["backend/domain/scoring.py", "backend/domain/completion.py", "backend/domain/badges.py", "backend/private/case_oracle.py", "backend/private/verdict_validator.py", "server/main.py", "server/catalog.py", "server/config.py", "src/api.ts", "src/main.jsx", "cases/completion_contracts/case_0042_v1.yaml"]

def main():
    h = hashlib.sha256(); files = []
    for name in PATHS:
        path = ROOT / name
        if not path.is_file(): raise SystemExit(f"missing runtime contract path: {name}")
        data = path.read_bytes().replace(b"\r\n", b"\n")
        h.update(name.encode() + b"\0" + data + b"\0"); files.append(name)
    print(json.dumps({"status":"PASS", "algorithm":"sha256", "digest":h.hexdigest(), "files":files}, indent=2))

if __name__ == "__main__": main()
