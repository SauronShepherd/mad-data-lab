# MDL-03 closure audit

Generated: 2026-08-26

## Verdict

**MDL-03 is not 100% closed.** The current repository contains working protocol, orchestration, deployment, and evidence components. Local implementation and deterministic gates are now green; authenticated live-evaluation, exact-head deployment/CI, and final release identity gates remain open. The report must remain `IN_PROGRESS`.

## Evidence snapshot

| Area | Current state | Closure state |
|---|---|---|
| Strict MDL-3 contract gate | 29/29 checks pass against current runtime digest, including art preflight and production derivatives | PASS |
| Local Python suite | 152 passed, 1 warning | PASS |
| Genie configuration read-back | Authenticated export captured; digest `ad8418446a24e0d1e17768ff981141027f75f9cfea4c183b030e17e6bedd8fef` | PASS |
| Deployment | Databricks deployment `01f1a13e70ea15119a15e59c93c04fad` succeeded | PASS, identity reconciliation required |
| Deployed smoke | PASS | PASS |
| Deployed soak | 10/10 PASS | PASS |
| Live 30-attempt benchmark | 30/30 failed by timeout in latest recorded run | OPEN / BLOCKING |
| Final implementation identity | Report says `NOT_FROZEN`; worktree is dirty | OPEN / BLOCKING |
| A05/A07 assets | 10 implementation-owned candidates recorded; 6 transparent A05 sprites, 4 opaque A07 environments, contact sheets, preflight, and 2 selected production derivatives | PASS |
| Final CI/post-merge evidence | Not present for the final identity | OPEN |

## P0 — production implementation defects

These must be fixed before a live benchmark can be considered meaningful:

1. Keep the canonical boundary and domain pending-decision orchestration covered by the current route path.
2. Keep the live adapter validating Genie responses against the server-derived allowed Experiment set, never a tuple-position golden answer.
3. Preserve the pending first decision and consume it atomically on the first `/next`; later turns derive the allowed set from server state and validated evidence.
4. Maintain integration coverage proving alternate legal selection and invalid-ID rejection without state mutation.
5. Re-run the authenticated live benchmark against the final frozen implementation; the recorded pre-fix 0/30 result remains stale evidence.

## P1 — authenticated live evaluation

1. Run all 30 benchmark IDs against the authenticated replacement Genie space.
2. Use fresh conversations for each sequence and genuine two-turn `GNEXT-*` cases.
3. Use the bounded submission/polling implementation and record per-attempt status, latency, conversation/message IDs, repair count, and failure reason.
4. Grade protocol validity, allowed selection, Instrument/target, evidence correctness, state safety, and security refusals.
5. Require all critical cases to pass and emit immutable JSON plus JUnit XML.
6. Bind the result to implementation SHA, runtime digest, Genie contract digest, live-config digest, MDL-2 digest, corpus hash, and batch ID.

## P1 — final identity and deployment evidence

1. Commit the final runtime-affecting implementation and record its exact SHA in `MDL-3-report.md`.
2. Ensure the smoke and soak artifacts reference that same SHA and all matching digests.
3. Prove the Databricks deployment source snapshot corresponds to that identity.
4. Run final-head CI and post-merge verification.
5. Remove or regenerate stale release artifacts that refer to previous deployments, old SHAs, or failed pre-fix runs.

## P2 — implementation-owned A05/A07 assets

Human approval is **not** a closure prerequisite under the agreed workflow. The implementation still needs:

1. A05 derived Genie poses.
2. A07 Hypothesis Chamber assets.
3. The required candidate slots, provenance/prompt hashes, contact sheets, previews, transparency and dimension checks.
4. Selection of production derivatives with review assets excluded from the shipped package.
5. Optional final human revision before submission.

## P2 — final release gates

Run from the final frozen identity:

- `python -m pytest -q` with no required skips/xfails.
- Clean `npm ci`, typecheck, and production build.
- Browser/UI contract tests.
- Security, accessibility, dependency, architecture, OpenAPI, traceability, MDL-1, and MDL-2 gates.
- MDL-3 protocol, lifecycle, fake-adapter, evaluation, configuration, deployment, and evidence gates.
- Sanitized-report scan with no secrets, private truth, signed URLs, or chain-of-thought.

## Closure sequence

The correct order is:

1. Fix the canonical production-path migration and allowed-set defect.
2. Add and pass the corresponding integration tests.
3. Generate A05/A07 implementation-owned assets and preflight evidence.
4. Freeze the final commit and digests.
5. Deploy that exact identity.
6. Run smoke and 10-journey soak.
7. Run the authenticated 30-attempt benchmark.
8. Run final-head CI and all release gates.
9. Update `docs/iterations/MDL-3-report.md` to `COMPLETE` only when every artifact references the same identity and no pending item remains.
