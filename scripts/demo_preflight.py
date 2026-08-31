"""Short, deterministic preflight for a Case #042 demo recording."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> dict[str, object]:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    return {"command": command, "status": "PASS" if result.returncode == 0 else "FAIL", "output": (result.stdout + result.stderr)[-1200:]}


def main() -> int:
    checks = [
        run([sys.executable, "scripts/docs_preflight.py"]),
        run([sys.executable, "scripts/validate_mdl3_contract.py", "--strict"]),
        run([sys.executable, "scripts/mdl2_sql_preflight.py"]),
        run([sys.executable, "scripts/assets_gate.py"]),
        run([sys.executable, "scripts/audio_preflight.py"]),
    ]
    payload = {"status": "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL", "checks": checks}
    report = ROOT / "release-report" / "MDL-5" / "demo-preflight.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
