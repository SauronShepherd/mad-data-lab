"""Local static security gate for synthetic-data and closed-control invariants."""
from __future__ import annotations

from pathlib import Path
import re
import sys
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_MARKERS = ('truth_json', 'primary_cause', 'primary_component', 'secondary_cause', 'expected_path_json', 'allowed_final_status_json', 'case_truth')
SECRET_PATTERNS = (r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', r'(?i)\b(?:databricks_pat|oauth_secret|api_key)\s*[:=]\s*["\']', r'(?i)\bBearer\s+[A-Za-z0-9_\-]{20,}')


def scan_repository() -> None:
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\\0")
    candidates = [ROOT / name for name in tracked if name and name != "scripts/security_gate.py" and (ROOT / name).is_file()]
    forbidden_files = [p for p in candidates if p.name.lower() in {'.env', '.env.local', '.env.production'} or p.suffix.lower() in {'.pem', '.key', '.p12'}]
    assert not forbidden_files, f"credential files present: {forbidden_files}"
    for path in candidates:
        text = path.read_text(encoding='utf-8', errors='ignore')
        assert not any(re.search(pattern, text) for pattern in SECRET_PATTERNS), f"secret-like pattern found: {path}"


def main() -> None:
    scan_repository()
    source_files = [*ROOT.glob("server/**/*.py"), *ROOT.glob("src/**/*"), *ROOT.glob("resources/**/*.json"), *ROOT.glob("sql/**/*.sql"), *ROOT.glob("data/fixtures/public/**/*.json")]
    source = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in source_files if path.is_file())
    assert not re.search(r"(?i)(databricks_pat|api[_-]?key|client_secret|password\s*=)", source), "secret-like source pattern found"
    frontend = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in ROOT.glob("src/**/*") if path.is_file())
    assert "CASE_TRUTH" not in frontend and "primary_component" not in frontend
    assert "eval(" not in frontend and "new Function(" not in frontend
    assert "dangerouslySetInnerHTML" not in frontend
    assert "case_id" in source and "registered" in source
    public_files = list(ROOT.glob("data/fixtures/public/**/*.json"))
    for path in public_files:
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        assert not any(marker in text for marker in PRIVATE_MARKERS), f'private truth leaked: {path}'
    for path in ROOT.glob("dist/**/*"):
        if path.is_file() and path.suffix.lower() in {'.js', '.html', '.css'}:
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
            assert not any(marker in text for marker in PRIVATE_MARKERS), f'private truth leaked in build: {path}'
    print("security gate: PASS")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(f"security gate: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
