"""Capture and hash the authenticated Genie space configuration."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--space-id", default=os.getenv("GENIE_SPACE_ID"))
    parser.add_argument("--profile", default=os.getenv("DATABRICKS_CONFIG_PROFILE", "sda"))
    parser.add_argument("--output", default="release-report/MDL-3/genie-live-config.json")
    args = parser.parse_args()
    if not args.space_id:
        raise SystemExit("--space-id or GENIE_SPACE_ID is required")
    from databricks.sdk import WorkspaceClient

    space = WorkspaceClient(profile=args.profile).genie.get_space(
        space_id=args.space_id,
        include_serialized_space=True,
    )
    serialized = getattr(space, "serialized_space", None)
    if not serialized:
        raise SystemExit("authenticated Genie read-back did not include serialized_space")
    if not isinstance(serialized, str):
        serialized = str(serialized)
    canonical = json.dumps(json.loads(serialized), sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    payload = {"status": "PASS", "space_id": args.space_id, "profile": args.profile, "genie_live_config_sha256": digest, "serialized_space": json.loads(serialized)}
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "genie_live_config_sha256": digest}, indent=2))


if __name__ == "__main__":
    main()
