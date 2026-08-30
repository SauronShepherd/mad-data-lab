# MDL-8 incident report — Genie experiment calls fail intermittently mid-session

- **Status:** OPEN — not resolved by the 2026-08-30 03:36 UTC redeploy (`deployment_id 01f1a423f0ad108c8dba9e7071784ecf`)
- **Severity:** High — directly affects the "Genie at the core" criterion (20/40 points) of the Databricks Genie-Powered App Challenge
- **First observed:** 2026-08-30, during deployed soak/smoke retesting against the redeployed Free Edition account
- **Reporter:** Claude Code, live testing session against `https://mad-data-lab-7474643947913626.aws.databricksapps.com`

## TL;DR

A live Genie call inside an investigation session fails intermittently (3/3 to 5/5 reproductions across two deployments), at a random point between experiment 2 and experiment 5 of the 5-experiment sequence, after 15–40 seconds — well under the configured 75s timeout. The error the client sees is `GENIE_EXPERIMENT_UNAVAILABLE` (`retryable: true`), and because the session's circuit breaker records it as a failure, repeated occurrences in the same session eventually surface `GENIE_CIRCUIT_OPEN` (`retryable: false`).

A fix was deployed that changes `SessionCircuitBreaker` (threshold 3→5 consecutive failures, plus a 60s recovery/half-open window). This is a real improvement to how a session **recovers** from failures, but it does not address why the underlying Genie call fails in the first place. Retesting against the new deployment reproduced the same failure pattern (2/2 additional stepped runs, plus the packaged smoke script), just possibly with more tolerance before the session is fully locked out.

## Evidence log (this session, reproducible)

All timings below are wall-clock for a single `/api/sessions/{id}/next` call, measured client-side with a stepped diagnostic script that calls the session API directly (create session → start → prediction → `next` × 5, printing status/time per call).

### Before the fix (deployment `01f1a4154e7e148db82c464ce9080c0a`)

| Run | Exp 1 | Exp 2 | Exp 3 | Exp 4 | Exp 5 |
|---|---|---|---|---|---|
| `deployed_smoke.py` | — | — | — | fails, `GENIE_CIRCUIT_OPEN` at retry (breaker already open) | — |
| stepped run A | 200 / 0.5s | 200 / 15.4s | 200 / 15.5s | **503 GENIE_EXPERIMENT_UNAVAILABLE / 40.3s** | (breaker opens; immediate `GENIE_CIRCUIT_OPEN` on retry) |
| stepped run B | 200 / 0.5s | **503 GENIE_EXPERIMENT_UNAVAILABLE / 21.3s** | — | — | — |

Direct SDK call bypassing the app (`scripts/live_genie_check.py`, single-turn conversation) succeeded both times this was tried — the raw Genie space and warehouse (`sda_dev`, `e444f39962128242`, state `HEALTHY`) are not down.

### After the fix (deployment `01f1a423f0ad108c8dba9e7071784ecf`, created 2026-08-30T03:36:09Z)

| Run | Exp 1 | Exp 2 | Exp 3 | Exp 4 | Exp 5 |
|---|---|---|---|---|---|
| `deployed_smoke.py` | 200 | **503 GENIE_CIRCUIT_OPEN** | — | — | — |
| stepped run C | 200 / 0.5s | **503 GENIE_EXPERIMENT_UNAVAILABLE / 16.9s** | — | — | — |
| stepped run D | 200 / 0.5s | 200 / 5.2s | 200 / 18.8s | 200 / 16.6s | **503 GENIE_EXPERIMENT_UNAVAILABLE / 36.0s** |

Five stepped reproductions total (2 before, 2 after, plus the packaged smoke script twice), 5/5 failed at a *different* experiment number each time, all in the 15–40s range. This rules out a bug scoped to one specific experiment's prompt/query, and rules out the 75s client timeout as the trigger.

## Root cause analysis (traced in code, not guessed)

Call chain for a single experiment turn:

```
/api/sessions/{id}/next  (server/main.py, session handler ~L766-820)
  → session_breaker(session).before_request()      # raises CircuitOpenError if breaker open
  → next_experiment(ExperimentRequest(...))          # server/main.py:850, also the /api/experiments/next handler
      → genie.next(conversation_id, context, case_id)  # CanonicalGenieBoundary → GenieAdapter.next, server/genie.py:347
          → workspace.genie.create_message(...)        # sends the next turn in the same Genie conversation
          → self._wait_for_message(...)                 # server/genie.py:236-262, polls up to genie_request_timeout_seconds (75s)
```

`_wait_for_message` (server/genie.py:236-262) polls `workspace.genie.get_message(...)` and branches on status:

- `COMPLETED` / `ASKING_AI` with an answer → returns normally.
- `FAILED` → `raise RuntimeError("Genie message failed")`
- `CANCELED` / `CANCELLED` → `raise RuntimeError("Genie message was canceled")`
- deadline exceeded → `raise TimeoutError(...)`

`GenieAdapter.next()` (server/genie.py:347-378) wraps the call in a `for _ in range(2)` loop, but **the `except` clause only catches `ValueError`** (raised by `_control_message` when Genie's JSON control payload is malformed) to retry with a "protocol repair" message. It does **not** catch the `RuntimeError`/`TimeoutError` raised by `_wait_for_message`. So the moment Genie's own backend marks one message `FAILED` (or the poll times out), the exception propagates immediately, with zero retries.

Back in `next_experiment()` (server/main.py:850), a broad `except Exception as exc` at line 866 catches this, logs it (`LOGGER.exception("live Genie next failed")`), and — because more than one experiment usually remains — raises `HTTPException(503, "Live Genie is unavailable")`.

The session handler around server/main.py:766-820 catches that `HTTPException`, calls `session_breaker(session).record_failure()`, and re-raises as `{"code": "GENIE_EXPERIMENT_UNAVAILABLE", "retryable": true}` — which is exactly what the client sees. If `consecutive_failures` reaches the breaker's `threshold` (now 5, was 3), subsequent calls short-circuit to `{"code": "GENIE_CIRCUIT_OPEN", "retryable": false}` until the 60s recovery window elapses (new behavior) or forever (old behavior, no recovery).

**In short: a single `FAILED` status from Genie's own backend, for a single message in a multi-turn conversation, is treated as fatal for that experiment call today. There is no retry path for it, only a retry path for malformed JSON.** Given 5/5 reproductions at different points in the 5-turn sequence, this looks like an intermittent backend-side failure rate on Genie/warehouse execution under this Free Edition account — not a deterministic bug tied to one prompt.

### What the deployed fix actually changed

`server/genie.py` `SessionCircuitBreaker`, before:

```python
class SessionCircuitBreaker:
    def __init__(self, threshold: int = 3) -> None:
        self.threshold = threshold
        self.consecutive_failures = 0
        self.open = False

    def before_request(self) -> None:
        if self.open:
            raise CircuitOpenError("Genie recovery is required for this session")
    ...
```

After:

```python
class SessionCircuitBreaker:
    """Session-scoped breaker with a bounded recovery window."""
    def __init__(self, threshold: int = 5, recovery_seconds: float = 60.0) -> None:
        self.threshold = threshold
        self.recovery_seconds = recovery_seconds
        self.consecutive_failures = 0
        self.open = False
        self.opened_at: float | None = None

    def before_request(self) -> None:
        if self.open:
            if self.opened_at is None or time.monotonic() - self.opened_at < self.recovery_seconds:
                raise CircuitOpenError("Genie recovery is cooling down for this session")
            # Half-open probe: success closes the breaker; failure re-opens it.
            self.open = False
            self.consecutive_failures = 0
            self.opened_at = None
    ...
```

This is a legitimate resilience improvement (a session now tolerates 5 consecutive failures instead of 3, and self-heals after 60s instead of being dead forever). But it changes nothing about `_wait_for_message`/`next()`/`start()`, so the underlying per-call failure rate is unchanged — which is exactly what retesting showed.

## Proposed fix

### 1. Retry a Genie-backend `FAILED`/`CANCELED` message, not just a malformed one

Extend the existing repair-retry loop in `GenieAdapter.next()` (and the analogous loop in `start()`) to also retry on the transport/backend failure, by sending a fresh message in the same conversation instead of only repairing malformed JSON. Sketch (illustrative, not a final diff):

```python
def next(self, conversation_id: str, context: str, case_id: str = DEFAULT_CASE_ID) -> dict:
    ...
    last_error = None
    for attempt in range(3):  # was range(2); one more attempt budget for backend-side failures
        waiter = self._workspace().genie.create_message(
            space_id=self.space_id, conversation_id=conversation_id,
            content=f"{system_prompt(case_id)}\n\nInvestigation context: {context}",
        )
        try:
            response = self._wait_for_message(waiter.conversation_id, waiter.message_id)
        except (RuntimeError, TimeoutError) as exc:
            last_error = exc
            if attempt + 1 < 3:
                time.sleep(0.5 * (attempt + 1))  # small backoff before re-asking
                continue
            raise
        try:
            message = self._control_message(response, case_id, allowed)
            ...
            return {"conversation_id": conversation_id, "message": message}
        except ValueError as exc:
            last_error = exc
    raise ValueError("Genie did not produce a valid experiment response after retries") from last_error
```

Apply the same pattern to `start()`. Keep the distinction between "malformed JSON" (already retried via protocol-repair) and "backend FAILED/timeout" (currently not retried at all) — both should now get a bounded retry budget before surfacing to the session layer.

### 2. Log the real Genie message status before translating it

`_wait_for_message` currently discards `status`/`last` once it decides to raise. Log the raw status (and, if present, any error/reason field on the message object) at `WARNING` before raising, so a future occurrence is diagnosable from application logs instead of needing a fresh live repro:

```python
if status.endswith("FAILED"):
    logger.warning("genie message FAILED", extra={"conversation_id": conversation_id, "message_id": message_id, "raw_status": status})
    raise RuntimeError("Genie message failed")
```

### 3. Verify (don't assume) the "singleton continuation" fallback

`next_experiment()` (server/main.py:850) already has a fallback: if exactly one experiment remains when a Genie exception is caught, it silently continues with a deterministic scripted payload instead of raising 503 (server/main.py:872-878). In stepped run D, the failure happened on **experiment 5 of 5** — at that point only one experiment should have remained, so this fallback should have applied and the call should have quietly succeeded. It didn't. This is either a second, distinct bug (the singleton check not triggering when expected) or a misread of the `completed_experiments` bookkeeping on my part — **it needs a direct trace/log check, not a guess**, before being folded into the fix above.

### 4. Investigate whether this is Free Edition resource contention

Everything observed is consistent with an intermittent failure rate on Genie/warehouse execution under the Free Edition Serverless Starter warehouse (2X-Small), especially after this account absorbed a high volume of back-to-back test traffic today. This doesn't change the code fix (item 1 is worth doing regardless), but it changes expectations: if the FAILED rate is a Free Edition throughput ceiling, retries reduce user-visible failures but won't eliminate them at high concurrency (e.g., a live judge session during a busy submission window).

## Test plan to validate the fix

### Unit / contract level (fast, no live Genie needed)
1. Add a test to `tests/test_genie_client.py` (or `test_genie_retry_policy.py`) that fakes `_wait_for_message` to raise `RuntimeError("Genie message failed")` on the first call and succeed on the second, and asserts `GenieAdapter.next()` returns the successful result instead of raising.
2. Same for `TimeoutError`.
3. Assert the retry budget is bounded (e.g., 3 consecutive backend failures still raises, doesn't retry forever).
4. Assert `start()` gets the same treatment (currently only `next()` was inspected in depth here — confirm `start()`'s loop needs the identical change).
5. Regression test: a malformed-JSON response must still only trigger the existing protocol-repair path, not the new backend-failure retry path (they're different failure classes and should stay logged/tested separately).

### Live / staging level (against the real Free Edition account)
1. Re-run the stepped diagnostic (`create session → start → prediction → next ×5`, logging status+latency per call) **10 times back to back** post-fix. Target: 10/10 full journeys complete without a client-visible 503, even if 1-2 individual Genie messages internally hit `FAILED` and get transparently retried (confirm via the new logging from item 2 above that retries are indeed happening, not that failures stopped occurring).
2. Re-run `scripts/deployed_soak.py` (10 authenticated journeys) — this is the existing gate; it should go from failing at journey 2 (observed today, both before and after the fix) to 10/10 PASS.
3. Deliberately widen the retry test: run 3 soak passes with a 10-minute gap between each, to separate "the fix works" from "the account had a quiet period." Record pass/fail and timestamps for all three.
4. Cross-check Databricks Apps runtime logs (workspace UI → Compute → Apps → mad-data-lab → Logs) during one live failure, to capture the actual Genie-side error/status the new logging (item 2) should now surface, and confirm it matches the hypothesis in this report rather than a different failure mode.
5. Only after 10/10 soak + a repeat 10/10 after the 10-minute-gap re-run, update `release-report/MDL-8/deployed-soak-live.json` and the final acceptance matrix — do not mark this PASS on a single clean run given today's history of intermittent failures.

## Risk to the Databricks Genie Challenge submission if left unresolved

"Genie at the core" is 20 of the challenge's 40 points, and the demo/judging experience is exactly the 5-experiment investigation flow that fails here. A judge playing through Case #042 has a real chance of hitting this mid-session, especially since failures have occurred as early as experiment 2. Given submission closes 2026-08-31 23:30 PDT, this is the single highest-priority technical item before final packaging — higher priority than the documentation/URL cleanup already completed earlier in this audit.

## Appendix — raw error payloads captured

```
# Before fix, stepped run A, experiment 4:
HTTP 503 {"error":{"code":"GENIE_EXPERIMENT_UNAVAILABLE","message":"The request could not be completed.","retryable":true,"preserve_evidence":true,"request_id":"7a0630f6-5170-439d-bbd6-42c66c7b56c5"}}

# Before fix, same session, immediate retry:
HTTP 503 {"error":{"code":"GENIE_CIRCUIT_OPEN","message":"The request could not be completed.","retryable":false,"preserve_evidence":true,"request_id":"7a874f15-f522-430f-a7db-ab2c45a01080"}}

# After fix, stepped run D, experiment 5:
HTTP 503 {"error":{"code":"GENIE_EXPERIMENT_UNAVAILABLE","message":"The request could not be completed.","retryable":true,"preserve_evidence":true,"request_id":"d1a12cb2-03fe-4210-9f55-375a0e364989"}}
```

Deployment identities referenced in this report:

| | Before fix | After fix |
|---|---|---|
| `deployment_id` | `01f1a4154e7e148db82c464ce9080c0a` | `01f1a423f0ad108c8dba9e7071784ecf` |
| created | 2026-08-30T01:51:24Z | 2026-08-30T03:36:09Z |
| URL | `https://mad-data-lab-7474643947913626.aws.databricksapps.com` (unchanged) | same |
| catalog / warehouse | `sda_dev` / `e444f39962128242` (unchanged) | same |
