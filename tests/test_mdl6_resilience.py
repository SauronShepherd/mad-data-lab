from server.genie import GenieAdapter
import pytest


def test_genie_ask_retries_transient_transport_once():
    adapter = GenieAdapter(sleeper=lambda _: None)
    calls = []
    class Genie:
        def create_message_and_wait(self, **kwargs):
            calls.append(kwargs)
            if len(calls) == 1:
                raise ConnectionError("temporary")
            return type("Response", (), {"content": "recovered", "attachments": []})()
    adapter._client = type("Client", (), {"genie": Genie()})()
    assert adapter.ask("conversation", "hello") == "recovered"
    assert len(calls) == 2


@pytest.mark.parametrize("timeout", [5, 30])
def test_genie_waiter_times_out_without_accepting_incomplete_message(monkeypatch, timeout):
    now = [10.0]
    adapter = GenieAdapter(clock=lambda: now[0], sleeper=lambda seconds: now.__setitem__(0, now[0] + seconds))
    adapter._client = type("Client", (), {"genie": type("Genie", (), {
        "get_message": lambda self, **kwargs: type("Message", (), {"status": "EXECUTING", "attachments": []})()
    })()})()
    monkeypatch.setattr("server.genie.load_settings", lambda: type("Settings", (), {
        "genie_request_timeout_seconds": timeout, "genie_poll_interval_ms": 50
    })())
    with pytest.raises(TimeoutError, match="did not complete"):
        adapter._wait_for_message("conversation", "message")


def test_genie_failed_message_is_not_treated_as_success(monkeypatch):
    adapter = GenieAdapter(sleeper=lambda _: None)
    adapter._client = type("Client", (), {"genie": type("Genie", (), {
        "get_message": lambda self, **kwargs: type("Message", (), {"status": "FAILED", "attachments": []})()
    })()})()
    monkeypatch.setattr("server.genie.load_settings", lambda: type("Settings", (), {
        "genie_request_timeout_seconds": 30, "genie_poll_interval_ms": 50
    })())
    with pytest.raises(RuntimeError, match="failed"):
        adapter._wait_for_message("conversation", "message")
