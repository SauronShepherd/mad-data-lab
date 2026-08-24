"""Static accessibility gate for the React surface; runtime axe remains a deployment check."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    source = (ROOT / "src" / "main.jsx").read_text(encoding="utf-8")
    images = re.findall(r"<img\b[^>]*>", source)
    assert images and all(re.search(r"\balt=", image) for image in images), "all images need alt text"
    assert "aria-label=" in source and "role=\"status\"" in source, "interactive/status semantics missing"
    assert "htmlFor=\"genie-question\"" in source
    assert "aria-expanded" in source
    print("a11y gate: PASS (static semantics; runtime axe is deployment-only)")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(f"a11y gate: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
