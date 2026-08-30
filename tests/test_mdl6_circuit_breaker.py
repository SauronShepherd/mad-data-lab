import pytest

from server.genie import CircuitOpenError, SessionCircuitBreaker


def test_breaker_opens_after_three_consecutive_failures():
    breaker = SessionCircuitBreaker(threshold=3)
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


def test_breaker_allows_probe_after_recovery_window():
    breaker = SessionCircuitBreaker(threshold=1, recovery_seconds=0)
    breaker.record_failure()
    breaker.before_request()
    assert not breaker.open
    assert breaker.consecutive_failures == 0
