from pathlib import Path

import pytest

from backend.genie.config_digest import file_digest, genie_contract_digest, load_benchmark, render_agent_source


def test_locked_benchmark_contains_exact_30_attempts():
    corpus = load_benchmark()
    assert len(corpus["attempts"]) == 30
    assert corpus["attempts"][0]["id"] == "OBS-01"
    assert corpus["attempts"][-1]["id"] == "SEC-03"


def test_contract_digest_changes_when_instruction_changes(tmp_path: Path):
    original = tmp_path / "a.txt"
    original.write_text("one", encoding="utf-8")
    first = file_digest(original)
    original.write_text("two", encoding="utf-8")
    assert file_digest(original) != first
    assert len(genie_contract_digest()) == 64


def test_benchmark_validator_rejects_missing_or_reordered_ids(tmp_path: Path):
    path = tmp_path / "bad.yaml"
    path.write_text("version: 1\nattempts: [{id: OBS-01}]\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_benchmark(path)


def test_agent_source_renderer_allows_valid_identifiers_and_rejects_injection():
    rendered = render_agent_source(catalog="sda_dev", schema="mad_data_lab")
    assert rendered["curated_sources"][0]["identifier"].startswith("sda_dev.mad_data_lab_curated.")
    with pytest.raises(ValueError):
        render_agent_source(catalog="sda_dev;DROP TABLE x", schema="mad_data_lab")
    with pytest.raises(ValueError):
        render_agent_source(catalog="sda_dev", schema="mad_data_lab.raw")
