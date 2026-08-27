from scripts.security_gate import scan_repository


def test_repository_has_no_credential_files_or_secret_patterns():
    scan_repository()
