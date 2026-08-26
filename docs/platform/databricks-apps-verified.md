# Databricks Apps platform verification baseline

verified_at_utc: 2026-08-25T00:00:00Z
verifier: repository planning baseline
runtime_python: "3.11"
runtime_node: "22.16"
port_environment: DATABRICKS_APP_PORT
genie_environment: GENIE_SPACE_ID
auth_mode: default Databricks App identity
github_auth: workload identity federation / OIDC
shutdown_budget_seconds: 15
app_file_budget_mb: 10

## Required operational consequences

- [ ] Revalidate these values against current official Databricks documentation before deployment.
- [x] Production launcher accepts the Databricks-provided port contract.
- [x] Genie identity is configuration-driven; credentials are not stored in source.
- [ ] Deployment proves runtime App identity permissions independently from CI deployment identity.
- [ ] Deployment proves exact resolved commit/runtime digest parity.
- [ ] Shutdown smoke proves bounded SIGTERM handling.

Official references:

- https://docs.databricks.com/aws/en/dev-tools/databricks-apps/system-env
- https://docs.databricks.com/aws/en/dev-tools/databricks-apps/dependencies
- https://docs.databricks.com/aws/en/dev-tools/databricks-apps/app-runtime
- https://docs.databricks.com/aws/en/dev-tools/databricks-apps/genie
- https://docs.databricks.com/aws/en/dev-tools/databricks-apps/resources
- https://docs.databricks.com/aws/en/dev-tools/databricks-apps/cicd-github-actions
