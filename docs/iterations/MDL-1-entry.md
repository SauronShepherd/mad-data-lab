# MDL-1 Entry Gate

status: BLOCKED_PREDECESSOR_AND_EXTERNAL_CLOSURE_EVIDENCE
iteration: MDL-1
recorded_at_utc: 2026-08-26T00:00:00Z

This is an auditable entry record, not a completion claim. Local implementation may proceed, but MDL-1/MDL-2 closure remains blocked until the external evidence below is supplied and independently verified.

| ID | Decision | Evidence | Status | Blocking note |
|---|---|---|---|---|
| MDL1-ENTRY-001 | Definitive V3 source and iteration contracts were read; repository contract fingerprints are recorded in the implementation reports. | `docs/BUILD_PLAN_MDL1_MDL2_MDL3.md`, `docs/iterations/MDL-1-report.md` | PASS_LOCAL | Canonical source archive is not present in this checkout. |
| MDL1-ENTRY-002 | Intended Git remote/base identity is not verifiable from the current workspace. | `git remote -v` / `git rev-parse` required | BLOCKED | Human must provide the accepted repository remote and `main` evidence. |
| MDL1-ENTRY-003 | Branch push/PR access is not verifiable. | GitHub push/PR probe required | BLOCKED | External GitHub access/evidence missing. |
| MDL1-ENTRY-004 | GitHub Actions enablement and required checks | `.github/workflows/` intentionally removed | NOT_APPLICABLE | Project uses local gates and direct Databricks CLI verification. |
| MDL1-ENTRY-005 | Databricks workspace/app and Free Edition target are identified. | `docs/platform/databricks-apps-verified.md`; app `mad-data-lab` | PASS_LOCAL | Free Edition attestation still requires external closure evidence. |
| MDL1-ENTRY-006 | Databricks CLI profile `sda` is authenticated and the app is addressable. | sanitized CLI probes; app id `ee09bcf7-9b74-4860-946a-7ddaf18db9c8` | PASS_LOCAL | App start is currently blocked by Free Edition daily compute quota. |
| MDL1-ENTRY-007 | Human artwork approver is not identified in repository evidence. | `docs/approvals/MDL-1-art.md` | BLOCKED | Human approver must approve exact production bytes. |
| MDL1-ENTRY-008 | Candidate generation and technical preflight artifacts exist. | `assets/review/MDL-1/`, `release-report/MDL-1/` | PASS_LOCAL | Human approval remains open. |
| MDL1-ENTRY-009 | Existing work is intentionally preserved rather than treated as clean. | current `git status --short` | BLOCKED | This implementation is being developed in a user-owned dirty worktree. |
| MDL1-ENTRY-010 | The application has a reproducible local baseline and automated gates. | `pytest`, frontend, container, and release reports | PASS_LOCAL | Exact-head CI/deployment evidence remains external. |

## Baseline evidence

- Python dependency lock: `pyproject.toml` + `uv.lock`; no production `requirements.txt`.
- Frontend lock: `package.json` + `package-lock.json`.
- Local test/build/release results are recorded under `release-report/`.
- Known external failures: GitHub closure evidence, human art approval, and Databricks Free Edition app-compute quota.
