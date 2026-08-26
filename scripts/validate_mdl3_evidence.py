"""Validate an MDL-3 live-evaluation artifact against explicit identities."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from backend.genie.evidence import EvidenceIdentity, validate_evidence_identity  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--implementation-sha", required=True)
    parser.add_argument("--genie-contract-digest", required=True)
    parser.add_argument("--genie-live-config-sha256", required=True)
    parser.add_argument("--mdl2-data-contract-digest", required=True)
    parser.add_argument("--case-hash", required=True)
    args = parser.parse_args()
    artifact = json.loads(args.artifact.read_text(encoding="utf-8"))
    expected = EvidenceIdentity(args.implementation_sha, args.genie_contract_digest, args.genie_live_config_sha256, args.mdl2_data_contract_digest, args.case_hash)
    validate_evidence_identity(artifact, expected)
    print(json.dumps({"status": "PASS", "artifact": str(args.artifact)}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, indent=2))
        raise SystemExit(1)
