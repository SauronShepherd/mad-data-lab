"""Render deterministic Genie Agent source config without applying remote state."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from backend.genie.config_digest import render_agent_source  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--output", default="release-report/MDL-3/rendered-agent.source.json")
    args = parser.parse_args()
    rendered = render_agent_source(catalog=args.catalog, schema=args.schema)
    destination = ROOT / args.output
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(rendered, indent=2) + "\n", encoding="utf-8")
    try:
        display_path = str(destination.relative_to(ROOT))
    except ValueError:
        display_path = str(destination)
    print(json.dumps({"status": "PASS", "output": display_path, "source_count": len(rendered["curated_sources"])}, indent=2))


if __name__ == "__main__":
    main()
