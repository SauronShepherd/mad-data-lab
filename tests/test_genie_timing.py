from types import SimpleNamespace

import pytest

from server.genie import GenieAdapter


def test_wait_for_message_uses_injected_clock_and_sleeper():
    now = [0.0]
    sleeps = []
    adapter = GenieAdapter(clock=lambda: now[0], sleeper=lambda seconds: (sleeps.append(seconds), now.__setitem__(0, now[0] + seconds)))
    adapter.space_id = "space"
    statuses = iter(["PENDING", "COMPLETED"])
    adapter._client = SimpleNamespace(genie=SimpleNamespace(get_message=lambda **_: SimpleNamespace(status=next(statuses), attachments=[], query_result=None)))
    result = adapter._wait_for_message("conversation", "message")
    assert result.status == "COMPLETED"
    assert sleeps and sleeps[0] == 1.0


def test_wait_for_message_has_bounded_timeout():
    now = [0.0]
    adapter = GenieAdapter(clock=lambda: now[0], sleeper=lambda seconds: now.__setitem__(0, now[0] + seconds))
    adapter.space_id = "space"
    adapter._client = SimpleNamespace(genie=SimpleNamespace(get_message=lambda **_: SimpleNamespace(status="PENDING", attachments=[], query_result=None)))
    with pytest.raises(TimeoutError):
        adapter._wait_for_message("conversation", "message")


@pytest.mark.parametrize("status", ["FAILED", "CANCELED", "CANCELLED"])
def test_wait_for_message_fails_fast_on_terminal_failure(status):
    adapter = GenieAdapter(clock=lambda: 0.0, sleeper=lambda _: pytest.fail("terminal failure must not poll"))
    adapter.space_id = "space"
    adapter._client = SimpleNamespace(
        genie=SimpleNamespace(
            get_message=lambda **_: SimpleNamespace(status=status, attachments=[], query_result=None)
        )
    )
    with pytest.raises(RuntimeError):
        adapter._wait_for_message("conversation", "message")
