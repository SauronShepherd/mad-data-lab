"""Build reproducible review contact sheets from candidate artwork."""
from __future__ import annotations

import json
import hashlib
import time
from pathlib import Path
from typing import Any
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]

def build(iteration: str) -> dict:
    plan = json.loads((ROOT / f"assets/review/{iteration}/art-generation-plan.json").read_text(encoding="utf-8"))
    slots = plan.get("slots")
    if slots is None:
        slots = [{"asset_id": item["asset_id"], "candidates": item["candidates"]} for item in plan["assets"]]
    entries: list[tuple[str, Path, Image.Image]] = []
    slot_sheets: dict[str, list[tuple[str, Path, Image.Image]]] = {}
    for slot in slots:
        slot_entries = []
        for rel in slot["candidates"]:
            raw_path = rel["path"] if isinstance(rel, dict) else rel
            path = ROOT / (raw_path if str(raw_path).startswith("assets/") else f"assets/review/{iteration}/{raw_path}")
            with Image.open(path) as image:
                converted: Image.Image = image.convert("RGB")
                item = (slot["asset_id"], path, converted)
                entries.append(item)
                slot_entries.append(item)
        slot_sheets[slot["asset_id"]] = slot_entries
    thumb_w, thumb_h, label_h = 320, 220, 34
    cols = 2
    rows = (len(entries) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), "white")
    draw = ImageDraw.Draw(sheet)
    for index, (asset_id, path, image) in enumerate(entries):  # type: ignore[assignment]
        x = (index % cols) * thumb_w
        y = (index // cols) * (thumb_h + label_h)
        image.thumbnail((thumb_w - 12, thumb_h - 12))
        sheet.paste(image, (x + (thumb_w - image.width) // 2, y + (thumb_h - image.height) // 2))
        draw.text((x + 8, y + thumb_h + 8), f"{asset_id} / {path.name}", fill="black")
    output = ROOT / f"release-report/{iteration}/art-contact-sheet.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, format="PNG", optimize=False)
    per_asset = {}
    for asset_id, items in slot_sheets.items():
        per_asset_dir = ROOT / f"assets/review/{iteration}/contact-sheets"
        per_asset_dir.mkdir(parents=True, exist_ok=True)
        per = Image.new("RGB", (len(items) * thumb_w, thumb_h + label_h), "white")
        per_draw = ImageDraw.Draw(per)
        for index, (_, path, image) in enumerate(items):  # type: ignore[assignment]
            image.thumbnail((thumb_w - 12, thumb_h - 12))
            x = index * thumb_w
            per.paste(image, (x + (thumb_w - image.width) // 2, (thumb_h - image.height) // 2))
            per_draw.text((x + 8, thumb_h + 8), f"{asset_id}-C{index + 1:02d} / {path.stem}", fill="black")
        per_path = per_asset_dir / f"{asset_id}.png"
        # Windows security/indexing tools can briefly hold an existing PNG;
        # retry the deterministic write once before failing the release gate.
        for attempt in range(2):
            try:
                per.save(per_path, format="PNG", optimize=False)
                break
            except OSError:
                if attempt == 1:
                    raise
                time.sleep(0.25)
        per_asset[asset_id] = {"path": per_path.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(per_path.read_bytes()).hexdigest(), "candidate_count": len(items)}
    return {"iteration": iteration, "status": "PASS", "candidate_count": len(entries), "path": output.relative_to(ROOT).as_posix(), "width": sheet.width, "height": sheet.height, "per_asset": per_asset}

def main() -> None:
    result = {iteration: build(iteration) for iteration in ("MDL-1", "MDL-2", "MDL-3", "MDL-4")}
    (ROOT / "release-report/art-contact-sheets.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
