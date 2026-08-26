"""Apply the repository-owned MDL-03 instructions to an existing Genie Space."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from databricks.sdk import WorkspaceClient

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True)
    parser.add_argument("--space-id", required=True)
    args = parser.parse_args()
    client = WorkspaceClient(profile=args.profile)
    current = client.genie.get_space(space_id=args.space_id, include_serialized_space=True)
    serialized = json.loads(current.serialized_space)
    instructions = (ROOT / "genie/instructions.md").read_text(encoding="utf-8").strip()
    serialized.setdefault("instructions", {})["text_instructions"] = [{
        "id": "a0420000000000000000000000000011",
        "content": [instructions],
    }]
    updated = client.genie.update_space(
        args.space_id,
        etag=current.etag,
        serialized_space=json.dumps(serialized, ensure_ascii=False, indent=2),
    )
    print(json.dumps({"status": "PASS", "space_id": updated.space_id, "etag": updated.etag}))


if __name__ == "__main__":
    main()
