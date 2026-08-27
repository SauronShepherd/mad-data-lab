"""Validate the recorded definitive-source baseline without inventing proof."""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    path = ROOT / "docs/traceability/source-baseline.json"
    if not path.exists():
        print(json.dumps({"status": "BLOCKED_SOURCE_BASELINE", "reason": "baseline record missing"})); return 1
    payload = json.loads(path.read_text(encoding="utf-8"))
    source = payload.get("source", {})
    pending = payload.get("pending", [])
    required = {"version": "3.0", "date": "2026-08-23", "sha256": "237570e5d62cee11e78ecced43c8449f62f53e7b547e9fe1bfbf4ed54eb0cc44"}
    if any(source.get(key) != value for key, value in required.items()):
        print(json.dumps({"status": "BLOCKED_SOURCE_DRIFT", "source": source})); return 1
    if pending:
        print(json.dumps({"status": "BLOCKED_SOURCE_BASELINE", "pending": pending, "sha256": source["sha256"]})); return 1
    print(json.dumps({"status": "PASS", "sha256": source["sha256"]})); return 0

if __name__ == "__main__": raise SystemExit(main())
