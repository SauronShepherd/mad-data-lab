from backend.mdl6_contract import ASSET_IDS, ACCESSIBILITY_IDS, CHAOS_IDS, PERFORMANCE_IDS, REQUIRED_TEST_IDS, SECURITY_IDS, REQUIREMENT_EXPECTATIONS, validate_catalog


def test_mdl6_catalog_has_all_specified_ids():
    validate_catalog()
    assert ACCESSIBILITY_IDS[0] == "AX-001" and ACCESSIBILITY_IDS[-1] == "AX-015"
    assert PERFORMANCE_IDS[0] == "PF-001" and PERFORMANCE_IDS[-1] == "PF-008"
    assert ASSET_IDS[0] == "AS-001" and ASSET_IDS[-1] == "AS-015"
    assert SECURITY_IDS[0] == "SEC-001" and SECURITY_IDS[-1] == "SEC-020"
    assert CHAOS_IDS[0] == "CH-001" and CHAOS_IDS[-1] == "CH-025"
    assert len(REQUIRED_TEST_IDS) == 83
    assert len(REQUIREMENT_EXPECTATIONS) == 58
    assert all(REQUIREMENT_EXPECTATIONS[item].strip() for item in REQUIREMENT_EXPECTATIONS)
