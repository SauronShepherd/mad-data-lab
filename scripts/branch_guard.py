"""Enforce the repository's unambiguous iteration branch names."""
from __future__ import annotations

import os
import re
import subprocess


def current_branch() -> str:
    return os.getenv("GITHUB_HEAD_REF") or subprocess.check_output(
        ["git", "branch", "--show-current"], text=True
    ).strip()


def main() -> None:
    branch = current_branch()
    if branch in {"main", "MDL-1", "MDL-2"} or re.fullmatch(r"MDL-[3-8]", branch):
        print(f"branch guard: PASS ({branch})")
        return
    raise SystemExit(f"branch guard: FAIL (unsupported branch name: {branch or 'DETACHED'})")


if __name__ == "__main__":
    main()
