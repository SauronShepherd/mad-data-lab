# MDL-3 iteration report

status: IN_PROGRESS
implementation_sha: fa5b5a4ae79e9cff826387dd4e1a9e2686b62ccb
runtime_digest: 4a039a1fbda603d51e100f59df417b54c25ce5ee1c99108830d36344b2b1fe1e
genie_contract_digest: a8cd0c4110005670f924f056e5e22cd3633abba9682d20e3ab8286b5f4d78fda
genie_live_config_sha256: 0aa19a3f70f0318058f467d9173208b46ec30ec2b2859a96e7ff52b5aef14ebd
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
- Exact-head CI: PASS for commit `8a0564616fe94f18ac3543d94d7e6943a9b496ae` (run `32996003084`; frontend, local-contracts, and container jobs).

## Pending closure evidence

- [x] Exact accepted implementation SHA after all runtime-affecting changes (`8a0564616fe94f18ac3543d94d7e6943a9b496ae`; exact-head CI passed).
- [x] Authenticated Genie Agent configuration export/read-back and `genie_live_config_sha256` (`release-report/MDL-3/genie-live-config.json`).
- [x] Protected 30-attempt live batch with immutable workflow artifact and JUnit result.
- [x] Databricks deployed smoke/soak against frozen implementation `9d54ef38786d852d4b42eff4a7dc2c3d02d5d294` and matching runtime/data/config evidence (`release-report/deployed-smoke.json`, `release-report/deployed-soak.json`).
- [x] A05/A07 implementation-owned review candidates, hashes, contact sheets, preflight, and selected production derivatives (`release-report/MDL-3/art-preflight.json`, `release-report/MDL-3/art-contact-sheet.png`, `public/assets/pixelart/dr-genie-mdl3.png`, `public/assets/pixelart/hypothesis-chamber.png`).
- [ ] Final-head CI and post-merge verification.

The report must not be changed to `COMPLETE` until every pending item has immutable evidence bound to the same accepted implementation identity.
