# MDL-4 platform verification

status: `PENDING_EXTERNAL_VERIFICATION`
iteration: `MDL-4`
recorded_at: `2026-08-27`

This record is intentionally not a completion claim. The local workspace can
verify the implementation and fixture-mode flow, but it cannot establish the
external platform facts that require authenticated workspace access or an
immutable deployment/CI artifact.

## Locally verified

- The authoritative MVP server runs one application process when session state
  is in memory (`server/run.py`).
- Session TTL and capacity are configurable, with the documented two-hour
  default (`server/config.py`).
- Fixture mode is explicit and is not used as a substitute for live evidence
  in closure mode.
- The MDL-4 local gate, contract checks, browser flow, and deterministic fake
  E2E flow pass on the current working tree.

## Pending external verification

- Authenticated Genie Conversation/Agent capability and workspace availability.
- Exact-head GitHub CI for the final pushed implementation SHA.
- Databricks deployment smoke/soak and one complete live Case #042 session.
- Immutable external evidence IDs and post-merge digest agreement.

Until those observations are recorded in immutable evidence, the MDL-4
closure status remains `IN_PROGRESS`/`BLOCKED_EXTERNAL`, never `COMPLETE`.
