"""Fail-closed guard for MDL closure evidence supplied by external systems."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    if len(sys.argv) != 3:
        print(json.dumps({"status": "FAIL", "reason": "usage: require_external_evidence.py ITERATION EVIDENCE_KIND"}))
        return 2
    iteration, kind = sys.argv[1:]
    manifest = ROOT / "release-report" / iteration / "external-evidence.json"
    if not manifest.exists():
        print(json.dumps({"status": "FAIL", "iteration": iteration, "kind": kind, "reason": "immutable external evidence manifest is missing"}))
        return 1
    try:
        payload = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "iteration": iteration, "kind": kind, "reason": f"invalid evidence manifest: {exc}"}))
        return 1
    item = payload.get(kind)
    if not isinstance(item, dict) or item.get("status") != "PASS" or not item.get("immutable_id"):
        print(json.dumps({"status": "FAIL", "iteration": iteration, "kind": kind, "reason": "evidence is absent, non-PASS, or lacks immutable identity"}))
        return 1
    print(json.dumps({"status": "PASS", "iteration": iteration, "kind": kind, "immutable_id": item["immutable_id"]}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
