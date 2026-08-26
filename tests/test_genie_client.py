from types import SimpleNamespace

import pytest

from backend.genie.client import GenieClientError, MessageState, normalize_message


def test_normalize_message_preserves_identity_and_state():
    result = normalize_message(SimpleNamespace(conversation_id="c1", message_id="m1", status="COMPLETED", content="ok"))
    assert result.conversation_id == "c1"
    assert result.message_id == "m1"
    assert result.state is MessageState.COMPLETED
    assert result.text == "ok"


def test_normalize_message_accepts_enum_like_sdk_status():
    class Status:
        value = "FAILED"

    result = normalize_message(SimpleNamespace(conversation_id="c1", message_id="m1", status=Status()))
    assert result.state is MessageState.FAILED


@pytest.mark.parametrize("response", [SimpleNamespace(status="UNKNOWN"), SimpleNamespace(status="COMPLETED")])
def test_normalize_message_rejects_unknown_state_or_missing_identity(response):
    with pytest.raises(GenieClientError):
        normalize_message(response, conversation_id="c1")
