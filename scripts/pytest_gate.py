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
    allowed_skip_markers = ("superseded by MDL-4", "CASE_001 is not enabled")
    skipped = [case for suite in suites for case in suite.findall(".//testcase") if case.find("skipped") is not None]
    disallowed_skips = [case for case in skipped if not any(marker in case.find("skipped").attrib.get("message", "") for marker in allowed_skip_markers)]
    counts = {"skipped": len(disallowed_skips), "xfailed": sum(int(suite.attrib.get("xfailed", "0")) for suite in suites), "xpassed": sum(int(suite.attrib.get("xpassed", "0")) for suite in suites)}
    if any(counts.values()):
        print(f"pytest gate: FAIL: disallowed results {counts}", file=sys.stderr)
        return 1
    total = sum(int(suite.attrib.get("tests", "0")) for suite in suites)
    print(f"pytest gate: PASS: {total} tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
