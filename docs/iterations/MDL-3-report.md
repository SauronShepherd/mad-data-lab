# MDL-3 iteration report

status: IN_PROGRESS
implementation_sha: NOT_FROZEN
runtime_digest: 30766cd2df28ec751d3224c17204b92be17fa5de05c03b6834b5349bc5c5010d
genie_contract_digest: 8e78b74e39bd9cd4936a2cc5b8b950cc3ebecee9b0a94890313b0277dc1ab9aa
genie_live_config_sha256: ad8418446a24e0d1e17768ff981141027f75f9cfea4c183b030e17e6bedd8fef
mdl2_data_contract_digest: 41f8e307c2420eb4b9e2627575572f32a0791e39e6ddedea5ed5199416cad471
benchmark_batch_id: mdl3-accepted-baseline

## Implemented local evidence

- Strict Pydantic protocol and exact control-object extraction: `backend/genie/protocol.py`.
- One-repair lifecycle and safe protocol/query failure separation: `backend/genie/lifecycle.py`.
- Pending first-Experiment decision persistence/consumption: `backend/genie/decisions.py`, `server/main.py`.
- Closed Experiment registry and permanent instructions: `genie/registry.json`, `genie/instructions.md`.
- Frozen 30-attempt corpus: `genie/benchmarks/mdl3-live.yaml`.
- Local contract gate: `release-report/MDL-3/contract-validation.json`.
- Local fixture benchmark JSON/JUnit: `release-report/MDL-3/benchmark.json`, `release-report/MDL-3/benchmark.junit.xml`.
- Live benchmark harness now binds implementation SHA, runtime digest, Genie config digest, MDL-2 data digest, and public Case #042 hash into its output; live execution still requires authenticated credentials.

## Pending closure evidence

- [ ] Exact accepted implementation SHA after all runtime-affecting changes.
- [x] Authenticated Genie Agent configuration export/read-back and `genie_live_config_sha256` (`release-report/MDL-3/genie-live-config.json`).
- [ ] Protected 30-attempt live batch with immutable workflow artifact and JUnit result.
- [x] Databricks deployed smoke/soak against frozen implementation `9d54ef38786d852d4b42eff4a7dc2c3d02d5d294` and matching runtime/data/config evidence (`release-report/deployed-smoke.json`, `release-report/deployed-soak.json`).
- [x] A05/A07 implementation-owned review candidates, hashes, contact sheets, preflight, and selected production derivatives (`release-report/MDL-3/art-preflight.json`, `release-report/MDL-3/art-contact-sheet.png`, `public/assets/pixelart/dr-genie-mdl3.png`, `public/assets/pixelart/hypothesis-chamber.png`).
- [ ] Final-head CI and post-merge verification.

The report must not be changed to `COMPLETE` until every pending item has immutable evidence bound to the same accepted implementation identity.
