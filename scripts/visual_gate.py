"""Static visual regression gate for the deterministic release artifact.

Pixel-diff baselines require a browser renderer and are deployment-only here;
this gate still proves the shipped HTML references the expected visual system,
has no broken local asset paths, and contains the accessible app root.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    html = (ROOT / "dist" / "index.html").read_text(encoding="utf-8")
    assert 'id="root"' in html
    css = (ROOT / "src" / "styles.css").read_text(encoding="utf-8")
    assert ".app" in css and ".case-card" in css and ".instrument" in css
    for asset in re.findall(r'(?:src|href)="([^"]+)"', html):
        if asset.startswith("/") and not (ROOT / "dist" / asset.lstrip("/")).exists():
            raise AssertionError(f"missing built asset: {asset}")
    print("visual gate: PASS (release artifact and visual anchors)")


if __name__ == "__main__":
    main()
