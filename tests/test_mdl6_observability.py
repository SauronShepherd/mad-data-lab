import json
import logging

from server.main import _safe_log_fields, log_event


def test_sensitive_observability_fields_are_redacted():
    result = _safe_log_fields({"session_id": "s1", "private_truth": {"cause": "hidden"}, "authorization": "secret"})
    assert result["session_id"] == "s1"
    assert result["private_truth"] == "[REDACTED]"
    assert result["authorization"] == "[REDACTED]"


def test_structured_event_logging_is_json(caplog):
    with caplog.at_level(logging.INFO, logger="mad_data_lab"):
        log_event("genie_request_failed", session_id="s1", diagnostic_code="GENIE_TIMEOUT")
    payload = json.loads(caplog.records[-1].message)
    assert payload["event"] == "genie_request_failed"
    assert payload["diagnostic_code"] == "GENIE_TIMEOUT"
