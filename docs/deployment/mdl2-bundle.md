# MDL-2 Databricks bundle

`databricks.yml` and `resources/mdl2.yml` define the staging deployment shape. The bundle is intentionally not applied from local development. Target `staging` uses CLI profile `sda`; deployment requires a valid authenticated profile and an explicitly supplied `validation_cluster_id`.

Current status: NOT_APPLIED_INVALID_SDA_REFRESH_TOKEN.
