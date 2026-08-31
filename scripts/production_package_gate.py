"""Fail-closed check for files that may enter a production application package."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = ("data/generation/private_specs", "data/fixtures/private")
PRIVATE_MARKERS = ("truth_json", "primary_cause", "primary_component", "secondary_cause", "case_truth")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--package-root", type=Path, help="assembled deployable package to inspect")
    args = parser.parse_args()
    root = args.root.resolve()
    package_root = args.package_root.resolve() if args.package_root else None
    failures: list[str] = []
    # The source checkout intentionally contains authoring truth.  The package
    # boundary is enforced by the two deployment ignore files below.
    ignore_text = (root / ".dockerignore").read_text(encoding="utf-8")
    databricks_ignore = (root / ".databricksignore").read_text(encoding="utf-8")
    for name, content in ((".dockerignore", ignore_text), (".databricksignore", databricks_ignore)):
        for relative in FORBIDDEN:
            if f"{relative}/" not in content:
                failures.append(f"{name} does not exclude {relative}/")
    if package_root:
        if not package_root.is_dir():
            failures.append(f"package root does not exist: {package_root}")
        else:
            for path in package_root.rglob("*"):
                if not path.is_file():
                    continue
                relative = path.relative_to(package_root).as_posix().lower()
                if any(relative == forbidden or relative.startswith(forbidden + "/") for forbidden in FORBIDDEN):
                    failures.append(f"forbidden path included in package: {relative}")
                try:
                    text = path.read_text(encoding="utf-8").lower()
                except (OSError, UnicodeDecodeError):
                    continue
                if any(marker in text for marker in PRIVATE_MARKERS):
                    failures.append(f"private marker included in package: {relative}")
    public = root / "data/fixtures/public/case_0042.bundle.json"
    try:
        serialized = json.dumps(json.loads(public.read_text(encoding="utf-8"))).lower()
        for marker in PRIVATE_MARKERS:
            if marker in serialized:
                failures.append(f"public bundle contains private marker: {marker}")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        failures.append(f"public bundle is unreadable: {exc}")
    result = {"status": "PASS" if not failures else "FAIL", "forbidden_paths": list(FORBIDDEN), "failures": failures}
    print(json.dumps(result, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
