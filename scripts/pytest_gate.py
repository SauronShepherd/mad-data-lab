"""Run pytest and reject skipped/xfail results in release-oriented CI."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--junitxml", default="release-report/pytest-gate.xml")
    args, pytest_args = parser.parse_known_args()
    output = Path(args.junitxml)
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, "-m", "pytest", "--junitxml", str(output), *pytest_args]
    result = subprocess.run(command, check=False)
    if result.returncode:
        return result.returncode
    root = ET.parse(output).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
    counts = {key: sum(int(suite.attrib.get(key, "0")) for suite in suites) for key in ("skipped", "xfailed", "xpassed")}
    if any(counts.values()):
        print(f"pytest gate: FAIL: disallowed results {counts}", file=sys.stderr)
        return 1
    total = sum(int(suite.attrib.get("tests", "0")) for suite in suites)
    print(f"pytest gate: PASS: {total} tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
