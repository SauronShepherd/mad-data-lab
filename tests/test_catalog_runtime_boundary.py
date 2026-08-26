from server.catalog import CANONICAL_PUBLIC_CATALOG, DEFAULT_CASE_ID


def test_runtime_catalog_boundary_validates_canonical_artifact():
    assert CANONICAL_PUBLIC_CATALOG["version"] == 1
    assert {case["id"] for case in CANONICAL_PUBLIC_CATALOG["cases"]} == {"CASE_0042", "CASE_0107"}
    assert DEFAULT_CASE_ID == next(case["id"] for case in CANONICAL_PUBLIC_CATALOG["cases"] if case["playable"])
