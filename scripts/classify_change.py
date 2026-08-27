"""Classify changed paths for selecting the appropriate release gates."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = {
    "frontend": ("src/", "public/", "index.html", "package.json", "package-lock.json", "vite.config", "tsconfig.json"),
    "backend": ("server/", "backend/", "pyproject.toml", "uv.lock"),
    "data": ("data/", "cases/", "sql/", "resources/genie/"),
    "deployment": (".github/", "app.yaml", "app.yml", "requirements.txt", "databricks.yml", "resources/", "Dockerfile", "docker-compose.yml"),
    "art": ("assets/", "public/assets/", "public/audio/", "docs/approvals/"),
    "release": ("release-report/", "docs/decisions/", "docs/iterations/", "docs/traceability/", "scripts/", "tests/"),
}


def changed_paths(base: str | None) -> list[str]:
    command = ["git", "diff", "--name-only"]
    if base:
        command.append(f"{base}...HEAD")
    else:
        command.extend(["HEAD^", "HEAD"])
    output = subprocess.check_output(command, cwd=ROOT, text=True)
    untracked = subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT, text=True)
    return sorted({path for path in (*output.splitlines(), *untracked.splitlines()) if path})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", help="base ref for a range diff; defaults to the previous commit")
    args = parser.parse_args()
    paths = changed_paths(args.base)
    scopes = {
        scope: sorted(path for path in paths if any(path == prefix or path.startswith(prefix) for prefix in prefixes))
        for scope, prefixes in RULES.items()
    }
    scopes = {scope: paths for scope, paths in scopes.items() if paths}
    known = {path for values in scopes.values() for path in values}
    unknown = sorted(set(paths) - known)
    result = {"head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(), "changed_paths": paths, "scopes": scopes, "unknown_paths": unknown, "status": "FAIL" if unknown else "PASS"}
    print(json.dumps(result, indent=2))
    if unknown:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
