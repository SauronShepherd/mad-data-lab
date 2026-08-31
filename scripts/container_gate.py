"""Build and smoke the packaged API, then verify graceful shutdown."""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    try:
        for attempt in range(2):
            try:
                run(["docker", "compose", "up", "-d", "--build", "api"])
                break
            except subprocess.CalledProcessError as exc:
                subprocess.run(["docker", "compose", "down"], cwd=ROOT, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if attempt == 1:
                    raise
                time.sleep(1)
        run([sys.executable, "scripts/container_smoke.py"])
        run([sys.executable, "scripts/container_shutdown_smoke.py"])
    finally:
        subprocess.run(["docker", "compose", "down"], cwd=ROOT, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("container gate: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
