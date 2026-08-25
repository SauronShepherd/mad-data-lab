"""Verify the packaged service honors SIGTERM within the platform window."""
from __future__ import annotations

import subprocess
import time


def main() -> None:
    container = subprocess.check_output(["docker", "compose", "ps", "-q", "api"], text=True).strip()
    if not container:
        raise SystemExit("shutdown smoke: API container is not running")
    subprocess.run(["docker", "kill", "--signal", "SIGTERM", container], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        running = subprocess.check_output(["docker", "inspect", "-f", "{{.State.Running}}", container], text=True).strip()
        if running.lower() != "true":
            print("container shutdown smoke: PASS (SIGTERM exit within 10 seconds)")
            return
        time.sleep(0.25)
    raise SystemExit("container shutdown smoke: FAIL (container remained running for 10 seconds)")


if __name__ == "__main__":
    main()
