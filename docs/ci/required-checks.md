# Required CI checks

The following stable categories are required for an accepted implementation head. A deployment check is required whenever deployment is invoked; no mandatory job may use `continue-on-error`.

| Check | Owns |
|---|---|
| `mdl1/repository-contract` | branch guard, manifests, traceability, documentation and architecture contracts |
| `mdl1/frontend` | typecheck, build, frontend/API terminology and accessibility contracts |
| `mdl1/backend` | pytest, mypy, OpenAPI and runtime contracts |
| `mdl1/security-static` | secret, private-truth, forbidden-path and dependency scans |
| `mdl1/art-preflight` | asset dimensions, formats, sizes, provenance and approval-byte checks |
| `mdl1/human-approval-gate` | explicit human approval evidence for subjective media |
| `mdl1/production-package-smoke` | container/package startup, port resolution and graceful shutdown |
| `mdl1/release-contract` | exact implementation identity, predecessor evidence and release-report consistency |

Executable configuration, dependency locks, prompts, SQL, assets and test infrastructure must not be able to bypass their owning check through path filters.
