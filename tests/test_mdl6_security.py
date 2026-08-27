from scripts.security_gate import scan_repository
from pathlib import Path


def test_repository_has_no_credential_files_or_secret_patterns():
    scan_repository()


def test_security_gate_has_production_bundle_and_frontend_sinks_covered():
    root = Path(__file__).parents[1]
    assert (root / "dist").is_dir()
    source = "\n".join(p.read_text(encoding="utf-8") for p in (root / "src").rglob("*") if p.is_file())
    assert "dangerouslySetInnerHTML" not in source
    assert "new Function(" not in source
    assert "eval(" not in source
    assert "CASE_TRUTH" not in source
