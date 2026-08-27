# ADR: MDL-4 private truth remains server-authoritative

Status: Accepted

## Decision

The MDL-4 client receives only the public case catalog, session projection,
earned evidence, and terminal verdict. Correctness, score eligibility, hidden
truth, and completion decisions remain in the server runtime under
`backend/private/` and the session ledger in `server/main.py`.

The client may request actions, but it cannot submit authoritative completion
lists, scores, truth values, or Genie prose as facts. The server validates
identifiers against the case contract, records immutable session events, and
reveals score only at conclusion/debrief.

## Consequences

- Fixture mode is explicit and cannot be selected by a deployed client.
- Live Genie failures remain retryable errors; the deployed path does not
  silently substitute a scripted result.
- Tests may use deterministic fixtures locally, while live-session evidence
  must come from the deployed API and is recorded separately.
