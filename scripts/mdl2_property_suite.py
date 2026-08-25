"""Deterministic MDL-2 property tier for local/CI release validation."""
from __future__ import annotations

import json
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from data.generation import generate_case
from data.generation.mutations import OPERATORS, apply_operator


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--seeds', type=int, default=10000)
    args = parser.parse_args()
    cases = 0
    operator_runs = 0
    signatures = set()
    template_counts = {'level1_clean': 0, 'level2_noisy': 0}
    release_hash = generate_case().content_hash
    for seed in range(args.seeds):
        case = generate_case(seed=seed, mode="property_test")
        assert case.public["property_seed"] == seed
        signatures.add(case.public['property_signature'])
        template_counts[case.public['property_template']] += 1
        cases += 1
        source = ({"business_key": f"K-{seed}", "amount": "1.00", "run_id": f"RUN-{seed}"},)
        for operator in OPERATORS:
            before = tuple(dict(row) for row in source)
            result = apply_operator(operator, source)
            assert result.operator_id == operator
            assert result.evidence["pure"] is True
            assert source == before
            assert result.evidence["affected_count"] == len(result.records)
            operator_runs += 1
    assert generate_case().content_hash == release_hash
    assert len(signatures) == args.seeds
    assert template_counts == {'level1_clean': args.seeds // 2, 'level2_noisy': args.seeds - args.seeds // 2}
    payload = {
        "status": "PASS",
        "seeds": cases,
        "templates": ["level1_clean", "level2_noisy"],
        "template_seed_split": template_counts,
        "operators": len(OPERATORS),
        "operator_runs": operator_runs,
        "release_artifact_unchanged": True,
    }
    out = ROOT / "release-report/MDL-2/property-suite.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
