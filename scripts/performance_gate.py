"""Deterministic local performance/package budgets for MDL-6."""
from __future__ import annotations
import gzip, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    dist = ROOT / "dist"
    if not dist.is_dir(): raise AssertionError("dist/ is missing; run npm build first")
    js = list(dist.rglob("*.js")); css = list(dist.rglob("*.css"))
    js_gzip = sum(len(gzip.compress(p.read_bytes(), compresslevel=9)) for p in js)
    css_gzip = sum(len(gzip.compress(p.read_bytes(), compresslevel=9)) for p in css)
    assert js_gzip < 700_000, f"compressed JS budget exceeded: {js_gzip}"
    assert css_gzip < 100_000, f"compressed CSS budget exceeded: {css_gzip}"
    oversized = [str(p.relative_to(ROOT)) for p in dist.rglob("*") if p.is_file() and p.stat().st_size >= 10_000_000]
    assert not oversized, f"packaged files exceed internal limit: {oversized}"
    print(json.dumps({"status":"PASS", "js_gzip_bytes":js_gzip, "css_gzip_bytes":css_gzip, "files":sum(1 for p in dist.rglob('*') if p.is_file())}, indent=2))

if __name__ == "__main__":
    try: main()
    except (AssertionError, OSError) as exc: print(f"performance gate: FAIL: {exc}", file=sys.stderr); raise SystemExit(1)
