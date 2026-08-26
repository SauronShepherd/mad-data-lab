import json
from pathlib import Path

import yaml
import pytest

from backend.domain.catalog import CatalogError, load_catalog, load_case_models


ROOT = Path(__file__).resolve().parents[1]


def test_catalog_has_track_and_only_case042_playable():
    catalog = yaml.safe_load((ROOT / "cases/catalog.yaml").read_text(encoding="utf-8"))
    assert catalog["track"] == "Track B - Creative Thinking"
    assert [case["id"] for case in catalog["cases"] if case["playable"]] == ["CASE_0042"]


def test_canonical_catalog_loader_validates_shape_and_identity():
    catalog = load_catalog()
    assert [case["id"] for case in catalog["cases"]] == ["CASE_0042", "CASE_0107"]
    assert [case.id for case in load_case_models()] == ["CASE_0042", "CASE_0107"]


def test_canonical_catalog_loader_rejects_duplicate_or_extra_fields(tmp_path):
    path = tmp_path / "catalog.yaml"
    path.write_text("version: 1\nbrand: MAD DATA LAB\ncases: []\n", encoding="utf-8")
    with pytest.raises(CatalogError, match="non-empty"):
        load_catalog(path)


def test_canonical_catalog_loader_rejects_private_truth_markers(tmp_path):
    path = tmp_path / "catalog.yaml"
    path.write_text(
        "version: 1\nbrand: MAD DATA LAB\ncases:\n"
        "  - {id: CASE_0001, number: 1, title: case_truth, metric: M, state: CORE, playable: true, "
        "expected: 1, observed: 1, deviation: 0, hypotheses: [H1], required_experiments: [RECONCILIATION]}\n",
        encoding="utf-8",
    )
    with pytest.raises(CatalogError, match="private truth"):
        load_catalog(path)


def test_genie_registry_is_versioned_and_closed():
    registry = json.loads((ROOT / "genie/registry.json").read_text(encoding="utf-8"))
    assert registry["registry_version"] == 2
    ids = [item["id"] for item in registry["experiments"]]
    assert len(ids) == len(set(ids)) == 5
    assert all(item["query_id"] and item["row_cap"] <= 100 for item in registry["experiments"])


def test_genie_agent_source_is_exact_sorted_curated_set():
    source = json.loads((ROOT / "genie/agent.source.json").read_text(encoding="utf-8"))
    identifiers = [item["identifier"] for item in source["curated_sources"]]
    assert source["version"] == 2
    assert identifiers == sorted(identifiers)
    assert len(identifiers) == len(set(identifiers)) == 6
    assert "case_truth" not in json.dumps(identifiers).lower()


def test_permanent_instructions_protect_truth_boundary():
    text = (ROOT / "genie/instructions.md").read_text(encoding="utf-8")
    assert "CASE_TRUTH" in text
    assert "arbitrary SQL" in text
    assert "schema_version" in text
