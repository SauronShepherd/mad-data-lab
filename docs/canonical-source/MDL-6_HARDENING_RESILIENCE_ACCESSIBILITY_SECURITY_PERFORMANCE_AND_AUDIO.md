# MDL-6 - Reliability Hardening, Error Handling, Accessibility, Security, Performance, Audio, and Operational Readiness

## Purpose

This iteration turns the polished happy path into a challenge-ready application that behaves correctly when Genie, SQL, network, assets, browser capabilities, or user interactions are imperfect.

MDL-6 is not a feature iteration. New analytical features or additional playable Cases are out of scope unless required to fix a release blocker. The objective is to eliminate fragile assumptions and complete the resilience, security, accessibility, performance, audio, packaging, and observability requirements in the V3 specification.

MDL-6 is complete only when all major failure modes are represented by automated tests, the deployed application fails honestly and recoverably, serious/critical accessibility issues are zero, hidden truth and secrets remain isolated, audio/media packaging passes, GitHub CI is green, Databricks staging deployment is healthy, and iteration-specific artwork is human-approved.

## Preconditions

Do not start MDL-6 until:

- MDL-5 merged to `main`;
- `main` CI green;
- all main Instruments and Evidence Explorer exist;
- visual regression/axe baseline exists;
- production no longer references obsolete board/fantasy-genie art;
- MDL-5 artwork approved;
- no uncommitted local changes.

## Branch and Git workflow - mandatory

```bash
git fetch origin --prune
git checkout main
git pull --ff-only origin main
test -z "$(git status --porcelain)"
git checkout -b MDL-6
```

Recommended commits:

```text
MDL-6: implement error taxonomy retry and resilience behavior
MDL-6: harden security permissions and secret isolation
MDL-6: complete accessibility responsive and reduced-motion behavior
MDL-6: add performance and asset packaging gates
MDL-6: integrate production audio controls and preflight
MDL-6: add approved badges and failure-state artwork
MDL-6: add iteration completion report
```

Push and PR:

```bash
git push -u origin MDL-6
gh pr create --base main --head MDL-6 --title "MDL-6 Reliability and release hardening" --body-file docs/iterations/MDL-6-report.md
```

## Scope lock

Allowed changes:

- bug fixes;
- resilience;
- retry/error states;
- logging/diagnostics;
- security/permissions;
- accessibility;
- responsive layout fixes;
- performance optimization;
- media/asset optimization;
- audio integration;
- test expansion;
- copy corrections needed for scientific precision.

Not allowed without explicit human/spec decision:

- implementing a new playable Case;
- adding a new LLM framework;
- introducing a new database solely for sessions;
- major React framework replacement;
- arbitrary visualization generation;
- large design-system dependency;
- changing Case #042 truth/numbers;
- relaxing required test gates to meet schedule.

## Error taxonomy

Implement stable domain/application error codes at minimum:

### Configuration

```text
GENIE_NOT_CONFIGURED
WAREHOUSE_NOT_CONFIGURED
MISSING_ENVIRONMENT_VARIABLE
```

### Genie

```text
GENIE_TIMEOUT
GENIE_FAILED
GENIE_MALFORMED_PROTOCOL
GENIE_UNSUPPORTED_EXPERIMENT
GENIE_QUERY_MISSING
GENIE_QUERY_FAILED
```

### Data

```text
CASE_NOT_FOUND
EVIDENCE_SCHEMA_MISMATCH
RECONCILIATION_FAILED
DATA_INVARIANT_FAILED
```

### State

```text
ILLEGAL_STATE_TRANSITION
SESSION_NOT_FOUND
DUPLICATE_ACTION
```

### Platform

```text
WAREHOUSE_PENDING
WAREHOUSE_QUOTA_EXHAUSTED
APP_RESOURCE_UNAVAILABLE
```

Every API error must use the stable response envelope and include a request ID.

Do not leak stack traces to browser responses.

## User-facing error behavior

For each error class define:

```text
human message
retryable true/false
preserve current evidence true/false
primary action
secondary action
telemetry diagnostic code
```

Examples:

### Genie timeout

- preserve current evidence;
- show that analysis took longer than expected;
- allow Retry when safe;
- do not advance Experiment state;
- do not silently insert a fixture answer.

### Reconciliation failed

- mark non-retryable for the current result unless requery can repair evidence;
- do not permit conclusion;
- show generic evidence validation failure rather than fabricated numbers;
- log exact residual privately.

### Warehouse quota unavailable

- preserve session;
- provide retry/later message;
- do not regenerate or mutate source data;
- offline verified mode only if explicitly enabled by operator, never automatically.

## Timeout and retry policy

Implement configured bounds equivalent to:

```text
initial Genie request timeout: 75s
poll interval: 1s with mild backoff after 10s
max protocol repair attempts: 1
safe SQL fallback query timeout: 45s
```

Tune only from measured staging behavior and record changes.

Automatically retry only:

- transient network failures;
- transient 429/5xx within bounded policy;
- expired query result where documented re-execution exists;
- one protocol repair.

Do not blindly repeat a completed analytical query or duplicate a state-changing action.

## Circuit-breaker-lite

Within a session, after three consecutive live Genie request failures:

- stop automatic retries;
- present an explicit recovery choice;
- offer verified fallback only if operator/config policy allows it;
- retain Genie conversation/message IDs for diagnostics;
- log the breaker event;
- do not corrupt existing evidence/history.

## Idempotency and race hardening

For every state-changing endpoint:

- reject/serialize duplicate concurrent `/next` calls;
- use idempotency keys where appropriate;
- ensure one Experiment event per successful logical action;
- ensure score/hint evidence events award only once;
- handle browser double-click;
- handle retry after network response loss without duplicate mutation.

Write concurrency tests around the session state store.

## Session loss / backend restart behavior

If sessions remain in memory:

- detect missing session after restart;
- return stable `SESSION_NOT_FOUND`/recovery response;
- frontend displays a clear Restart Investigation action;
- no stale local browser state should pretend an Experiment is still authoritative;
- preserve progression/preferences where safe.

Do not add persistent infrastructure solely to avoid this limitation unless it is already available with minimal risk.

## Structured observability

Finalize structured JSON logging.

Required events include:

```text
session_created
investigation_started
genie_request_started
genie_request_completed
genie_request_failed
protocol_repair_attempted
experiment_selected
experiment_completed
safe_fallback_used
evidence_inspected
hint_used
prediction_submitted
conclusion_validated
conclusion_rejected
session_completed
state_transition_error
circuit_breaker_opened
```

Include safe fields:

```text
request_id
session_id
case_id
experiment_id
instrument_id
duration_ms
fallback_used
genie_conversation_id
genie_message_id
diagnostic_code
```

Never log:

- OAuth/PAT/client secrets;
- authorization headers;
- raw hidden truth;
- private key material;
- unnecessary user identity.

## Security hardening

### Least privilege

Document and verify the app service principal only has required permissions:

- permission to run/use the Genie resource;
- CAN USE SQL warehouse;
- SELECT on needed public/curated evidence;
- SELECT on private Case truth only if the backend validator truly needs it.

The Genie resource must not have access to `case_truth`.

### Static secret scan

Run on every PR/main:

- PAT/token patterns;
- PEM/private keys;
- committed `.env`;
- OAuth secrets;
- suspicious Databricks credential fields.

### Dependency vulnerability scan

Block known critical exploitable vulnerabilities. Document any lower-severity accepted risk and why.

### Prompt/control safety

Automate tests proving:

- `show me case_truth` does not expose truth;
- `ignore all prior instructions` does not expand Experiment/Instrument allowlists;
- model HTML/JS is escaped;
- model-provided URL/code is never executed;
- user text cannot choose arbitrary tables;
- user business-key search cannot inject SQL;
- session Case cannot be changed through API input;
- evidence endpoints cannot cross Cases;
- production offline mode cannot be toggled by URL/query/body.

### Frontend safety

`dangerouslySetInnerHTML` is prohibited unless formally reviewed and allowlisted. Preferred: no usage.

All model text rendered as plain escaped text.

## Accessibility completion

### Document shell

Ensure frontend HTML has:

```text
<!doctype html>
<html lang="en">
viewport meta
descriptive title
```

### Form controls

- every label associated with its control;
- hypothesis prediction options keyboard accessible;
- buttons have descriptive accessible names;
- disabled/loading state communicated;
- error messages associated with the relevant control where applicable.

### Focus

- visible focus ring;
- logical tab order;
- modal/dialog focus trap when a true modal exists;
- Escape closes dismissible dialogs;
- focus restored to the trigger;
- no keyboard traps.

### Live regions

Use restrained `aria-live` only for meaningful status updates such as Experiment ready/error. Do not announce every decorative animation step.

### Data visualizations

Every chart has:

- textual summary;
- exact values;
- semantic table when practical;
- no color-only meaning.

### Audio control

Mute/unmute control communicates state to assistive technology.

### Reduced motion

Honor both:

```text
prefers-reduced-motion: reduce
user in-app reduced-motion preference
```

Persist the preference safely.

## Responsive completion

Remove remaining fixed-width assumptions.

Verify at:

```text
1600x900
1440x900
1280x720
390x844
```

No critical horizontal overflow.

At 390x844:

- Case Board works;
- primary Investigation action reachable;
- evidence table may use a responsive card/scroll treatment but remains operable;
- no essential content hidden solely due to viewport.

## Audio production and integration

The V3 spec requires long-form instrumental background music but only one final selected track should be packaged.

### Production behavior

- muted until user gesture / Enter Lab;
- persistent mute/unmute;
- default volume roughly 18-25%;
- fade in around 1.5s;
- fade out around 0.8s;
- loop;
- no required sound effects;
- autoplay rejection handled without error state.

### Audio file budget

Target final production asset:

```text
duration 330-510 seconds
file < 8.5MB
browser-supported codec
44.1kHz or higher
valid mono/stereo
integrated loudness approximately -22 to -12 LUFS
true peak below -1 dBTP preferred
no >4 second near-silence mid-track
```

The existing bundled audio can be retained only if it passes the technical and human listening gates and has appropriate licensing/ownership for submission.

If a new track is produced externally, store only the final approved production derivative in the app bundle.

### `scripts/audio_preflight.py`

Implement checks for:

- duration;
- decode integrity;
- channel count;
- sample rate;
- file size;
- silence gaps;
- loudness;
- peak.

Use ffprobe/ffmpeg where available or a documented equivalent.

## Performance hardening

### Build budgets

Track:

```text
JS compressed total target < 700KB if practical
CSS compressed target < 100KB
each production image normally < 1.5MB unless explicitly approved
final audio < 8.5MB
no individual app file > Databricks per-file limit
```

Do not block solely on a modest JS target miss if a required chart/library creates a reasonable increase, but fail on unreviewed regressions.

### Frontend performance

Measure:

- local production first meaningful UI < 2s on normal development machine;
- button feedback < 100ms;
- chart render < 300ms for demo data;
- Evidence Table 100 rows no main-thread stall, target < 500ms render;
- no N+1 evidence calls;
- avoid loading unused full-resolution art at boot.

### Deployed performance

Measure and record:

- `/api/health` warm target < 1s;
- app shell warm p50/p95;
- Genie latency p50/p95 from available staging runs;
- SQL query latency.

Do not make the build fail on one noisy external latency measurement; fail on severe regression or contract timeout violations.

## Asset packaging hardening

### Image preflight

Finalize `scripts/image_preflight.py`:

- manifest asset exists;
- expected dimensions;
- decode;
- alpha where needed;
- size budget;
- no unsupported profile;
- no accidental source files in bundle;
- production references only approved assets.

### Static file limit

Fail CI if any packaged file exceeds the platform file limit. Keep the stricter internal media budget.

### 404 behavior

If a decorative illustration fails to load:

- layout remains usable;
- alt/decorative semantics correct;
- data and controls remain visible;
- no broken-image icon overlaps critical UI.

If audio fails:

- app remains fully functional;
- audio control gracefully indicates unavailable/muted state;
- no repeated network/error loop.

## Tests required to close MDL-6

### Accessibility suite

Complete AX-001 through AX-015 across all primary screens.

Required:

```text
0 critical
0 serious
```

Also run keyboard-only E2E through a complete or critical Investigation path.

### Performance tests

Implement PF-001 through PF-008 as applicable:

- bundle size budget;
- local first meaningful UI;
- interaction feedback;
- chart render;
- Evidence Table 100 rows;
- deployed health;
- deployed shell measurements;
- no API N+1.

### Asset tests

Implement AS-001 through AS-015:

- manifest completeness;
- dimensions;
- alpha;
- decode;
- file-size budgets;
- no accidental source packages;
- final audio exists;
- duration range;
- audio file size;
- decode;
- loudness;
- true peak;
- silence gap;
- production asset paths.

### Security tests

Implement SEC-001 through SEC-020 from the V3 catalog.

Do not mark a security test complete because the feature "probably cannot happen". Demonstrate it programmatically or document why a specific platform permission test cannot be automated and provide the strongest available check.

### Chaos/resilience tests

Implement CH-001 through CH-025, including:

- Genie 5s latency;
- Genie 30s latency;
- Genie timeout;
- transient 500 then success;
- persistent 500;
- malformed JSON;
- wrong Case protocol;
- unsupported Experiment;
- missing query;
- SQL timeout;
- SQL empty result;
- SQL wrong columns;
- reconciliation mismatch;
- warehouse pending;
- quota unavailable;
- browser network loss;
- retry after restoration;
- illustration 404;
- audio 404;
- autoplay rejected;
- duplicate POST race;
- backend restart/session loss;
- corrupted local preferences;
- long evidence field;
- Unicode business key/title.

The expected behavior for each chaos case must be asserted, not only "does not crash".

### E2E reliability tests

Run/complete:

- E2E-015 Genie timeout;
- E2E-016 Genie failed;
- E2E-017 missing query;
- E2E-018 expired result recovery where supported;
- E2E-021 mobile-width basic operation;
- E2E-022 1440x900;
- E2E-023 1280x720;
- E2E-024 keyboard-only flow;
- E2E-027 double click;
- E2E-029 offline fixture banner when explicitly enabled in non-production;
- E2E-030 production offline mode disabled.

Run the deterministic fixture E2E suite repeatedly in CI or a soak job to reveal races.

## GitHub CI changes

By MDL-6, the main branch pipeline should approximate the V3 stages:

```text
1 validate repository
2 locked installs
3 static checks
4 unit/component tests
5 property/data tests
6 frontend build
7 asset/audio preflight
8 backend integration with fakes
9 E2E fixture suite
10 visual regression
11 accessibility
12 package/dependency/security audit
```

Real SQL and live Genie remain protected/quota-aware jobs but must be callable from GitHub.

### CI failure policy

- no `continue-on-error` for required jobs;
- no required job silently disabled on `MDL-6`;
- flaky tests must be fixed, not permanently retried until green;
- one diagnostic retry is acceptable for known external transient live tests, but final status must reflect actual failure if threshold not met.

## Artwork checkpoint - mandatory before iteration closure

This iteration creates achievement badges and the calm system-failure/loading background.

### MDL6-A14 - Achievement badge set

Generate four cohesive visual badge assets or a sheet that can be cleanly cropped. The first four visual motifs in the V3 asset guide are:

```text
1 beginner flask + one data spark
2 advanced metric dial + scientific star
3 microscope over record grid
4 skeptical shield deflecting warning triangle
```

Because the product has seven canonical badge rules, these four visuals may be reused/mapped only if the mapping is documented and visually unambiguous. If unique art is desired for all seven badges, generate three additional matching motifs in the same system, but do not invent new badge names.

Requirements:

- circular/enamel game achievement style;
- dark navy base;
- cyan/violet/amber/restrained coral accents;
- readable at 64px;
- transparent background;
- no words/letters/numbers/logos/watermark.

Do not bake badge names into images; names are HTML.

### MDL6-A16 - Loading/failure background

Prompt intent:

```text
Calm inactive module of the approved futuristic data laboratory during a temporary system pause. Instruments at low standby, soft cyan lights, no danger or damage, visually quiet center for real retry/error message. Premium enterprise stylized 3D, dark navy, no people, text, numbers, logos, or watermark.
```

Target: 1600x900.

### Automated preflight

Standard image checks plus:

- badge silhouettes readable at 64px;
- no generated letters;
- failure background never looks catastrophic/dangerous;
- no fake retry button in artwork;
- approved style consistency.

### Human approval gate

Create `docs/approvals/MDL-6-art.md`.

Human must approve:

- badge set/mappings;
- failure/loading background;
- final selected audio track separately in the same approval record or `MDL-6-audio.md`.

Human audio review rubric:

```text
laboratory identity
low fatigue
supports narration
memorable but not distracting
loopability
consistent energy
professional polish
```

Codex cannot mark art/audio APPROVED without explicit human approval.

## Databricks deployment gate

Deploy to staging via GitHub Actions after branch CI green.

Run automated staging scenarios for:

- normal health/shell;
- one live Genie Experiment;
- controlled timeout/error path if staging config supports fault injection;
- asset load;
- audio load without autoplay;
- reduced-motion config;
- no production offline mode;
- no secret fields in config/health;
- no hidden truth payload.

Capture structured logs and verify diagnostic request IDs correlate with errors.

## Manual deployment inspection

Human inspection after automation:

- keyboard-only basic navigation;
- reduced-motion experience;
- 1280x720 visual fit;
- 390x844 basic operability;
- audio starts only after user gesture and at low volume;
- mute works and persists;
- failure screen is calm/clear;
- retry messaging does not blame user;
- badge visuals match their HTML badge names;
- approved failure art integrates cleanly;
- no console errors during normal path.

Do not use this pass to prove security or analytical correctness; automated gates are authoritative.

## GitHub and merge closure

Run:

```bash
gh run list --branch MDL-6 --limit 30
gh pr checks --watch
```

All required jobs green.

Merge only after:

- security/accessibility/chaos/performance/asset tests green;
- art and audio human-approved;
- staging deployment green;
- manual deployment inspection accepted.

After merge, verify `main` CI and main deployment behavior.

## Required iteration report

Create `docs/iterations/MDL-6-report.md` containing:

- branch/PR/commit references;
- complete error taxonomy table;
- retry/circuit breaker policy;
- security test summary;
- axe summary;
- chaos test summary;
- performance/build-size summary;
- audio preflight results;
- asset preflight results;
- human art/audio approval links;
- staging deploy/smoke evidence;
- open risks deferred to RC iteration only.

## Definition of Done - MDL-6

- [ ] Branch `MDL-6` created from green merged MDL-5 `main`.
- [ ] Stable error taxonomy implemented.
- [ ] API never exposes stack traces.
- [ ] Retry behavior is bounded and idempotent.
- [ ] Circuit-breaker-lite implemented/tested.
- [ ] Duplicate concurrent actions cannot duplicate Experiments/scores.
- [ ] Session-loss behavior is explicit and non-corrupting.
- [ ] Structured observability complete without secrets/truth leakage.
- [ ] Least-privilege permissions documented and checked.
- [ ] SEC-001 through SEC-020 pass or have a documented platform-limited equivalent with human acceptance.
- [ ] Axe shows zero serious/critical issues.
- [ ] Keyboard navigation/focus/reduced-motion requirements pass.
- [ ] Mobile/basic responsive behavior passes.
- [ ] Audio technical preflight passes.
- [ ] Human approves final audio selection.
- [ ] Build/media performance budgets tracked and no unapproved regression remains.
- [ ] AS-001 through AS-015 pass.
- [ ] CH-001 through CH-025 pass.
- [ ] Required E2E resilience scenarios pass.
- [ ] GitHub CI is fully green.
- [ ] Databricks staging deploy/smoke green.
- [ ] MDL6-A14 badge art generated/preflighted.
- [ ] MDL6-A16 failure/loading art generated/preflighted.
- [ ] Human explicitly approves all MDL-6 artwork.
- [ ] Branch pushed and PR merged only after gates.
- [ ] `main` CI green after merge.
- [ ] Iteration report complete.

If any item is false, MDL-7 must not start.
