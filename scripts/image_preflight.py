"""Validate packaged raster assets against MDL-6 budgets."""
from pathlib import Path
import sys
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
APPROVED_LEGACY = {
    "Mad_Data_Lab.png", "decomposer.png", "dr-genie-mdl3.png", "hypothesis-chamber.png",
    "lab-hub.png", "reactor.png", "scanner.png", "board.png", "microscope.png", "telescope.png",
    "lab-mark.png", "dr-genie.png", "case-042.png",
}
def main() -> None:
    assets = list((ROOT / "public" / "assets").rglob("*.png"))
    if not assets: raise AssertionError("no packaged PNG assets")
    for path in assets:
        with Image.open(path) as image: image.verify()
        with Image.open(path) as image:
            if image.width > 2560 or image.height > 1440: raise AssertionError(f"dimensions exceed budget: {path}")
        if path.stat().st_size >= 1_500_000 and path.name not in APPROVED_LEGACY:
            raise AssertionError(f"unapproved image exceeds 1.5 MB: {path}")
    print(f"image preflight: PASS ({len(assets)} assets)")
if __name__ == "__main__":
    try: main()
    except (AssertionError, OSError) as exc: print(f"image preflight: FAIL: {exc}", file=sys.stderr); raise SystemExit(1)
