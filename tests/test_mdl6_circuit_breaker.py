import pytest

from server.genie import CircuitOpenError, SessionCircuitBreaker


def test_breaker_opens_after_three_consecutive_failures():
    breaker = SessionCircuitBreaker()
    for _ in range(2):
        breaker.before_request()
        breaker.record_failure()
    assert not breaker.open
    breaker.before_request()
    breaker.record_failure()
    assert breaker.open
    with pytest.raises(CircuitOpenError):
        breaker.before_request()


def test_success_resets_failure_count_and_closes_breaker():
    breaker = SessionCircuitBreaker(threshold=1)
    breaker.record_failure()
    assert breaker.open
    breaker.record_success()
    assert breaker.consecutive_failures == 0
    breaker.before_request()
