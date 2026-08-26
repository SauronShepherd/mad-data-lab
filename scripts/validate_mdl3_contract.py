"""Fail-closed deterministic MDL-3 repository contract gate."""
from __future__ import annotations

import argparse
import json
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.genie.config_digest import genie_contract_digest, load_benchmark
from backend.genie.query_registry import TRUSTED_QUERIES


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    checks: list[tuple[str, bool]] = []
    required = ("genie/instructions.md", "genie/registry.json", "genie/benchmarks/mdl3-live.yaml", "genie/agent.source.json", "backend/genie/protocol.py", "docs/traceability/mdl3-tests.csv", "docs/iterations/MDL-3-report.md")
    checks.extend((f"path:{path}", (ROOT / path).is_file()) for path in required)

    # Art is part of the MDL-03 release contract: review candidates must be
    # hash-bound and selected production derivatives must be present outside
    # the review tree. Keep this fail-closed so a stale/missing art report
    # cannot pass merely because the protocol files are healthy.
    art_report_path = ROOT / "release-report/MDL-3/art-preflight.json"
    try:
        art_report = json.loads(art_report_path.read_text(encoding="utf-8"))
        candidates = art_report.get("candidates", [])
        derivatives = art_report.get("production_derivatives", [])
        checks.extend([
            ("art:preflight-pass", art_report.get("status") == "CANDIDATES_PREFLIGHT_PASS"),
            ("art:exactly-10-candidates", art_report.get("candidate_count") == 10 and len(candidates) == 10),
            ("art:unique-candidate-ids", len({item.get("candidate_id") for item in candidates}) == 10),
            ("art:production-derivatives", len(derivatives) == 2 and all(
                item.get("exists") and len(item.get("sha256", "")) == 64
                and item.get("path", "").startswith("public/")
                and item.get("path", "").lower().endswith((".png", ".webp", ".jpg", ".jpeg"))
                for item in derivatives
            )),
        ])
    except (OSError, ValueError, json.JSONDecodeError):
        checks.extend([
            ("art:preflight-pass", False),
            ("art:exactly-10-candidates", False),
            ("art:unique-candidate-ids", False),
            ("art:production-derivatives", False),
        ])

    instructions = (ROOT / "genie/instructions.md").read_text(encoding="utf-8")
    checks.extend(
        [
            ("instructions:truth-boundary", "CASE_TRUTH" in instructions),
            ("instructions:no-arbitrary-sql", "arbitrary SQL" in instructions),
            ("instructions:protocol-version", "schema_version" in instructions),
        ]
    )
    registry = json.loads((ROOT / "genie/registry.json").read_text(encoding="utf-8"))
    experiments = registry.get("experiments", [])
    checks.append(("registry:query-ids-trusted", all(item.get("query_id") in TRUSTED_QUERIES for item in experiments)))
    ids = [item.get("id") for item in experiments]
    checks.extend(
        [
            ("registry:version-2", registry.get("registry_version") == 2),
            ("registry:unique-experiments", len(ids) == len(set(ids)) == 5),
            ("registry:bounded-queries", all(item.get("query_id") and 0 < item.get("row_cap", 0) <= 100 for item in experiments)),
            ("registry:no-private-truth", "case_truth" not in json.dumps(registry).lower()),
        ]
    )
    source = json.loads((ROOT / "genie/agent.source.json").read_text(encoding="utf-8"))
    identifiers = [item.get("identifier", "") for item in source.get("curated_sources", [])]
    serialized_identifiers = json.dumps(identifiers).lower()
    checks.extend(
        [
            ("source:version-2", source.get("version") == 2),
            ("source:exact-six-curated-views", len(identifiers) == len(set(identifiers)) == 6),
            ("source:sorted", identifiers == sorted(identifiers)),
            ("source:no-private-raw", not any(token in serialized_identifiers for token in ("case_truth", "raw.", "private."))),
        ]
    )
    corpus = None
    try:
        corpus = load_benchmark()
        checks.append(("benchmark:exact-30", len(corpus["attempts"]) == 30))
    except Exception as exc:
        checks.append((f"benchmark:valid ({exc})", False))
    checks.append(("protocol:strict-models", "extra=\"forbid\"" in (ROOT / "backend/genie/protocol.py").read_text(encoding="utf-8")))
    report = (ROOT / "docs/iterations/MDL-3-report.md").read_text(encoding="utf-8")
    checks.append(("report:not-falsely-complete", "status: COMPLETE" not in report or "PENDING" not in report))
    digest = genie_contract_digest()
    checks.append(("digest:sha256", len(digest) == 64 and all(char in "0123456789abcdef" for char in digest)))
    checks.append(("report:contract-digest-current", f"genie_contract_digest: {digest}" in report))
    runtime_digest = subprocess.check_output([sys.executable, "scripts/compute_runtime_digest.py"], cwd=ROOT, text=True).strip()
    checks.append(("report:runtime-digest-current", f"runtime_digest: {runtime_digest}" in report))
    failed = [name for name, passed in checks if not passed]
    result = {"status": "PASS" if not failed else "FAIL", "checks": len(checks), "failed": failed, "genie_contract_digest": digest}
    output = ROOT / "release-report/MDL-3"
    output.mkdir(parents=True, exist_ok=True)
    (output / "contract-validation.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if failed or (args.strict and corpus is None):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
