"""Fail-closed validation of exact-byte human artwork approval records."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] != "--iteration":
        print(json.dumps({"status": "FAIL", "reason": "usage: validate_human_approvals.py --iteration ITERATION"})); return 2
    iteration = sys.argv[2]
    path = ROOT / "docs/approvals" / f"{iteration}-art.md"
    if not path.exists():
        print(json.dumps({"status": "BLOCKED_HUMAN_APPROVAL", "iteration": iteration, "reason": "approval record missing"})); return 1
    text = path.read_text(encoding="utf-8")
    status = re.search(r"status\s*:\s*`?([A-Z_]+)", text, re.I)
    if not status or status.group(1).upper() != "APPROVED":
        print(json.dumps({"status": "BLOCKED_HUMAN_APPROVAL", "iteration": iteration, "reason": "exact-byte approval is not APPROVED"})); return 1
    print(json.dumps({"status": "PASS", "iteration": iteration})); return 0

if __name__ == "__main__": raise SystemExit(main())
