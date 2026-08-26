"""Record explicit human artwork selections without silently approving assets."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _plan(iteration: str) -> dict:
    return json.loads((ROOT / f"assets/review/{iteration}/art-generation-plan.json").read_text(encoding="utf-8"))


def _enforce_pixel_art(plan: dict) -> None:
    constraints = {str(item).lower() for item in plan.get("global_constraints", [])}
    required = {"pixel art only", "funny comedic pixel-art style"}
    if not required.issubset(constraints):
        raise SystemExit("art plan must require funny pixel art for every asset")


def _parse_selection(values: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise SystemExit(f"invalid selection {value!r}; use ASSET_ID=relative/candidate-path")
        asset_id, path = value.split("=", 1)
        if not asset_id or not path or asset_id in result:
            raise SystemExit(f"invalid or duplicate selection: {value!r}")
        result[asset_id] = path.replace("\\", "/")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iteration", choices=("MDL-1", "MDL-2"), required=True)
    parser.add_argument("--reviewer", required=True, help="Human reviewer identity; never defaults.")
    parser.add_argument("--selection", action="append", required=True, help="ASSET_ID=exact candidate path")
    args = parser.parse_args()
    if not args.reviewer.strip() or args.reviewer.strip().upper() in {"NOT_RECORDED", "UNKNOWN"}:
        raise SystemExit("a real human reviewer identity is required")

    plan = _plan(args.iteration)
    _enforce_pixel_art(plan)
    selections = _parse_selection(args.selection)
    slots = {slot["asset_id"]: slot for slot in plan["slots"]}
    if set(selections) != set(slots):
        raise SystemExit(f"selections must cover exactly {sorted(slots)}")

    approved: dict[str, dict[str, str]] = {}
    for asset_id, path_text in selections.items():
        slot = slots[asset_id]
        candidates = {candidate.replace("\\", "/") for candidate in slot["candidates"]}
        if path_text not in candidates:
            raise SystemExit(f"{asset_id}: selection is not a listed candidate: {path_text}")
        path = ROOT / path_text
        if not path.is_file():
            raise SystemExit(f"{asset_id}: candidate does not exist: {path_text}")
        approved[asset_id] = {
            "path": path_text,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }

    output = {
        "iteration": args.iteration,
        "status": "APPROVED",
        "human_reviewer": args.reviewer.strip(),
        "approved_at_utc": datetime.now(timezone.utc).isoformat(),
        "selected_exact_byte_hashes": approved,
        "source_plan": f"assets/review/{args.iteration}/art-generation-plan.json",
    }
    target = ROOT / "docs/approvals" / f"{args.iteration}-art-approval.json"
    target.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "APPROVED", "iteration": args.iteration, "output": str(target.relative_to(ROOT))}, indent=2))


if __name__ == "__main__":
    main()
