# MDL-4 implementation report

Status: `IN_PROGRESS`

Local identity evidence: branch `MDL-4`, current head is maintained on the pushed
remote branch. The worktree contains pre-existing unrelated MDL-2/3 generated
changes, which are intentionally preserved. Exact-head CI remains a separate
closure requirement; authenticated deployment evidence is recorded below.

Architecture mapping is recorded in
`docs/decisions/ADR-mdl4-architecture-mapping.md`.

Implemented and locally verified:

- server-authoritative Case #042 flow through `PLAYER_PREDICTION_FINAL`,
  `CONCLUDING`, and explicit `DEBRIEF`;
- separate initial/final predictions with private correctness scoring;
- pure score reducer, five-family completion predicate, evidence entitlements,
  explicit lineage/high-value inspection, and canonical badge derivation;
- safe session projection with hidden investigation score;
- configurable session TTL/capacity and stale revision rejection;
- frontend final-prediction and Debrief actions;
- refresh recovery from the authoritative session projection, including the
  current Experiment result and terminal verdict/Debrief states;
- repeatable fake-E2E and gameplay digest scripts.
- expiration recovery creates a fresh session ID and marks the expired session terminal;
- A03/A06 review candidates generated and SHA-256 recorded; final visual inspection is deferred to the user’s end-of-task review.

Local evidence:

- `scripts/run_mdl4_fake_e2e.py`: PASS, Case #042 reaches `DEBRIEF` with perfect-path score `1000`;
- `tests/browser/app.spec.ts` Case #042 visible flow: PASS, final prediction → verdict → Debrief;
- browser reload recovery within the Case #042 flow: PASS;
- `scripts/openapi_contract_gate.py`: PASS;
- `npm run typecheck`: PASS;
- `npm run build`: PASS;
- MDL-4 tests: PASS;
- all seven locked score scenarios: PASS;
- `scripts/run_iteration_gate.py --iteration MDL-4 --mode local`: PASS across
  contract, OpenAPI, frontend privacy contract, local chaos, MDL-4 tests,
  fake E2E, frontend typecheck, and build;
- MDL-4 fake-E2E: PASS (`DEBRIEF`, score 1000);
- focused MDL-4 evidence/game-flow suite: 17 passed, 1 capability-dependent skip;
- full historical suite: 168 passed, 7 explicitly allowed compatibility skips;
- current gameplay digest: `eb619a20de43749062eefa5e003ddad9b3a2a3e289e278cee4601e47f93c3664`.

Deployment smoke and post-deployment inspection are verified: five unique
experiments, explicit evidence inspections, final prediction, `DEBRIEF`, and
score `1000`. Closure remains pending exact-head CI. Final A03/A06 visual
inspection is an end-of-task review and is not a closure gate.
