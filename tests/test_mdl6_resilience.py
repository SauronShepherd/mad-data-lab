from server.genie import GenieAdapter


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
