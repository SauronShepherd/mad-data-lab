"""Fail-closed local preflight for the judge-facing documentation surface."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "docs/README.md", "docs/JUDGE_GUIDE.md", "docs/GENIE_AT_THE_CORE.md",
    "docs/ARCHITECTURE.md", "docs/CASE_0042_WALKTHROUGH.md",
    "docs/TESTING_AND_RELEASE.md", "docs/SECURITY_AND_TRUST_BOUNDARIES.md",
    "docs/DEPLOYMENT.md", "docs/DEMO_SCRIPT.md", "docs/KNOWN_LIMITATIONS.md",
    "docs/implementation_audit.md", "docs/community_article_draft.md",
    "docs/JUDGE_SCREENSHOTS.md",
)


def main() -> int:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    documents = {path: (ROOT / path).read_text(encoding="utf-8") for path in REQUIRED if (ROOT / path).is_file()}
    text = "\n".join(documents.values())
    placeholders = sorted(set(re.findall(r"\b(?:TODO|TBD|PLACEHOLDER|YOUR_[A-Z_]+)\b", text, re.I)))
    local_paths = sorted(set(re.findall(r"(?:[A-Za-z]:\\|/Users/|/home/|C:\\\\Users\\\\)[^\s)`]+", text)))
    canonical = all(value in text for value in ("125.0M", "118.2M", "-€6.8M", "-€5.9M", "€0.0M"))
    broken = []
    for path, document in documents.items():
        for link in re.findall(r"\]\(([^)#]+)\)", document):
            if link.startswith(("docs/", "../", "./")) and not (ROOT / path).parent.joinpath(link).resolve().exists():
                broken.append(f"{path}:{link}")
    failed = {"missing": missing, "placeholders": placeholders, "local_paths": local_paths, "broken_links": broken, "canonical_values": not canonical}
    failed = {key: value for key, value in failed.items() if value}
    print({"status": "FAIL" if failed else "PASS", "documents": len(REQUIRED), "failed": failed})
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
