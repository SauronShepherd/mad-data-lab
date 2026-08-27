from types import SimpleNamespace
from unittest.mock import patch

import pytest

from server.genie import GenieAdapter


def test_start_allows_only_one_repair_attempt():
    adapter = GenieAdapter()
    adapter.space_id = "space"
    response = SimpleNamespace(conversation_id="c", message_id="m")
    workspace = SimpleNamespace(genie=SimpleNamespace(
        start_conversation=lambda **_: response,
        create_message=lambda **_: response,
    ))
    with patch.object(adapter, "_workspace", return_value=workspace), patch.object(adapter, "_wait_for_message", return_value=SimpleNamespace(content="invalid", attachments=[], conversation_id="c", message_id="m")), patch.object(adapter, "_control_message", side_effect=ValueError("invalid")) as control:
        with pytest.raises(ValueError):
            adapter.start("CASE_0042")
    assert control.call_count == 2
