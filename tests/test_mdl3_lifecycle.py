from backend.genie.lifecycle import GenieTurn, TurnFailure


def valid():
    return '{"schema_version":"1.0","case_id":"CASE_0042","observation":"signal","hypotheses":[{"id":"H1","title":"Source","status":"POSSIBLE","evidence":[]}],"selected_experiment":{"id":"SNAPSHOT_DIFF","question":"Inspect","target_component":"V2"},"instrument":{"id":"SNAPSHOT_DIFF","title":"Snapshot"},"next_action":"RUN_EXPERIMENT","scientist_line":"Inspect V2."}'


def test_one_repair_then_success_and_query_runs_after_validation():
    calls = []
    outputs = iter(["not json", valid()])
    turn = GenieTurn(
        active_case_id="CASE_0042",
        allowed_experiments={"SNAPSHOT_DIFF"},
        instrument_for_experiment=lambda _: {"SNAPSHOT_DIFF"},
        request=lambda _: next(outputs),
        repair=lambda message: calls.append(message) or valid(),
        trusted_query=lambda response: {"rows": 1},
    )
    result = turn.run()
    assert result.failure is None
    assert result.repair_count == 1
    assert result.query_result == {"rows": 1}
    assert len(calls) == 1


def test_second_invalid_protocol_never_runs_query():
    query_calls = []
    turn = GenieTurn(
        active_case_id="CASE_0042",
        allowed_experiments={"SNAPSHOT_DIFF"},
        instrument_for_experiment=lambda _: {"SNAPSHOT_DIFF"},
        request=lambda _: "invalid",
        repair=lambda _: "still invalid",
        trusted_query=lambda response: query_calls.append(response),
    )
    result = turn.run()
    assert result.failure == TurnFailure.PROTOCOL_INVALID_AFTER_REPAIR
    assert query_calls == []


def test_query_failure_preserves_valid_selection_but_is_not_committed():
    turn = GenieTurn(
        active_case_id="CASE_0042",
        allowed_experiments={"SNAPSHOT_DIFF"},
        instrument_for_experiment=lambda _: {"SNAPSHOT_DIFF"},
        request=lambda _: valid(),
        repair=lambda _: valid(),
        trusted_query=lambda _: (_ for _ in ()).throw(RuntimeError("warehouse unavailable")),
    )
    result = turn.run()
    assert result.response is not None
    assert result.failure == TurnFailure.QUERY_FAILED_AFTER_VALID_SELECTION
