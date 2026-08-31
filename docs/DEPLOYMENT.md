# Deployment

Build with `npm run build`. The Databricks App deployment path is defined by `databricks.yml` and the repository deployment scripts. Resource-bound SQL and Genie configuration are supplied by the target environment, not committed secrets.

Before calling a deployment release-ready, verify `/api/health`, the Case catalog, Case #042 start/session flow, Genie interaction, Experiments, evidence, verdict, and debrief. Record the deployed source SHA/runtime digest, authenticated smoke result, and ten-run Case #042 soak result in immutable release evidence.
