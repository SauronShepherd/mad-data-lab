from types import SimpleNamespace

import pytest

from server.genie import GenieAdapter
from server.genie import system_prompt


def _response(text: str):
    return SimpleNamespace(content=text, attachments=[], conversation_id="c1", message_id="m1")


def _valid():
    return '{"schema_version":"1.0","case_id":"CASE_0042","observation":"signal","hypotheses":[{"id":"H1","title":"Source","status":"POSSIBLE","evidence":[]}],"selected_experiment":{"id":"SNAPSHOT_DIFF","question":"Inspect V2","target_component":"V2"},"instrument":{"id":"SNAPSHOT_DIFF","title":"Snapshot"},"next_action":"RUN_EXPERIMENT","scientist_line":"Inspect V2."}'


def test_live_adapter_validates_v3_response_before_legacy_fallback():
    adapter = GenieAdapter()
    adapter._client = SimpleNamespace()
    result = adapter._control_message(_response(_valid()), "CASE_0042", {"COMPONENT_DECOMPOSITION", "SNAPSHOT_DIFF"})
    assert result["schema_version"] == "1.0"
    assert result["selected_experiment"]["id"] == "SNAPSHOT_DIFF"
    assert result["source"] == "genie"


def test_live_adapter_rejects_invalid_v3_response():
    adapter = GenieAdapter()
    adapter._client = SimpleNamespace()
    with pytest.raises(ValueError, match="invalid V3"):
        adapter._control_message(_response(_valid().replace('"CASE_0042"', '"CASE_0107"')), "CASE_0042", {"COMPONENT_DECOMPOSITION", "SNAPSHOT_DIFF"})


def test_live_adapter_accepts_any_currently_allowed_experiment_not_a_golden_answer():
    adapter = GenieAdapter()
    adapter._client = SimpleNamespace()
    result = adapter._control_message(_response(_valid()), "CASE_0042", {"SNAPSHOT_DIFF"})
    assert result["selected_experiment"]["id"] == "SNAPSHOT_DIFF"


def test_production_prompt_requests_v3_protocol():
    prompt = system_prompt("CASE_0042")
    assert "schema_version 1.0" in prompt
    assert "selected_experiment" in prompt
    assert "arbitrary SQL" in prompt
