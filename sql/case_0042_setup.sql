-- MAD DATA LAB Case #042 curated Genie-facing data.
-- CASE_TRUTH is deliberately absent from this script and must remain application-only.

CREATE SCHEMA IF NOT EXISTS sda_dev.mad_data_lab;

CREATE OR REPLACE TABLE sda_dev.mad_data_lab.case_observations (
  case_id STRING,
  public_number INT,
  title STRING,
  metric_id STRING,
  metric_label STRING,
  entity_id STRING,
  period STRING,
  expected_eur_m DECIMAL(12, 2),
  observed_eur_m DECIMAL(12, 2),
  deviation_eur_m DECIMAL(12, 2),
  difficulty STRING
);

INSERT OVERWRITE sda_dev.mad_data_lab.case_observations VALUES
('CASE_0042', 42, 'The Missing €6.8M', 'CAPITAL_AVAILABLE', 'Capital Available', 'PT001', '2026-07', 125.00, 118.20, -6.80, 'LEVEL_2');

CREATE OR REPLACE TABLE sda_dev.mad_data_lab.component_deltas (
  case_id STRING,
  component_id STRING,
  previous_value_eur_m DECIMAL(12, 2),
  current_value_eur_m DECIMAL(12, 2),
  sign INT,
  contribution_delta_eur_m DECIMAL(12, 2)
);

INSERT OVERWRITE sda_dev.mad_data_lab.component_deltas VALUES
('CASE_0042', 'V1', 100.10, 98.90, 1, -1.20),
('CASE_0042', 'V2', 30.00, 24.10, 1, -5.90),
('CASE_0042', 'V3', 5.10, 4.80, -1, 0.30),
('CASE_0042', 'V4', 0.00, 0.00, 1, 0.00);

CREATE OR REPLACE TABLE sda_dev.mad_data_lab.snapshot_changes (
  case_id STRING,
  component_id STRING,
  change_type STRING,
  record_count INT,
  net_impact_eur_m DECIMAL(12, 2),
  previous_snapshot STRING,
  current_snapshot STRING
);

INSERT OVERWRITE sda_dev.mad_data_lab.snapshot_changes VALUES
('CASE_0042', 'V2', 'MODIFIED', 23, -5.20, 'SNAP_20260802_0900', 'SNAP_20260803_0900'),
('CASE_0042', 'V2', 'REMOVED', 2, -0.80, 'SNAP_20260802_0900', 'SNAP_20260803_0900'),
('CASE_0042', 'V2', 'ADDED', 5, 0.10, 'SNAP_20260802_0900', 'SNAP_20260803_0900');

CREATE OR REPLACE TABLE sda_dev.mad_data_lab.evidence_records (
  case_id STRING,
  business_key STRING,
  component_id STRING,
  previous_amount_eur_m DECIMAL(12, 2),
  current_amount_eur_m DECIMAL(12, 2),
  impact_eur_m DECIMAL(12, 2),
  change_type STRING,
  source_name STRING,
  previous_snapshot STRING,
  current_snapshot STRING
);

INSERT OVERWRITE sda_dev.mad_data_lab.evidence_records VALUES
('CASE_0042', 'TX-004291', 'V2', 4.20, 0.00, -4.20, 'MODIFIED', 'finance_reporting_source', 'SNAP_20260802_0900', 'SNAP_20260803_0900');

CREATE OR REPLACE TABLE sda_dev.mad_data_lab.formula_versions (
  case_id STRING,
  formula_id STRING,
  formula_text STRING,
  formula_hash STRING,
  effective_snapshot STRING
);

INSERT OVERWRITE sda_dev.mad_data_lab.formula_versions VALUES
('CASE_0042', 'CAPITAL_AVAILABLE_V1', 'V1 + V2 - V3 + V4', '58d7_demo_case042', 'SNAP_20260802_0900'),
('CASE_0042', 'CAPITAL_AVAILABLE_V1', 'V1 + V2 - V3 + V4', '58d7_demo_case042', 'SNAP_20260803_0900');

CREATE OR REPLACE TABLE sda_dev.mad_data_lab.dq_signals (
  case_id STRING,
  issue_id STRING,
  rule_name STRING,
  severity STRING,
  affected_rows INT,
  estimated_overlapping_impact_eur_m DECIMAL(12, 2),
  overlaps_component_id STRING,
  status STRING
);

INSERT OVERWRITE sda_dev.mad_data_lab.dq_signals VALUES
('CASE_0042', 'DQ_0042_01', 'DUPLICATE_BUSINESS_KEY', 'MEDIUM', 5, -0.30, 'V2', 'OPEN');

CREATE OR REPLACE VIEW sda_dev.mad_data_lab.v_case042_experiment_decomposition AS
SELECT c.*, d.component_id, d.contribution_delta_eur_m,
       ROUND(ABS(d.contribution_delta_eur_m) / ABS(c.deviation_eur_m) * 100, 2) AS deviation_share_pct
FROM sda_dev.mad_data_lab.case_observations c
JOIN sda_dev.mad_data_lab.component_deltas d USING (case_id)
WHERE c.case_id = 'CASE_0042';

CREATE OR REPLACE VIEW sda_dev.mad_data_lab.v_case042_snapshot_diff AS
SELECT *, SUM(net_impact_eur_m) OVER (PARTITION BY case_id, component_id) AS component_net_impact_eur_m
FROM sda_dev.mad_data_lab.snapshot_changes
WHERE case_id = 'CASE_0042';

CREATE OR REPLACE VIEW sda_dev.mad_data_lab.v_case042_formula_check AS
SELECT case_id, COUNT(DISTINCT formula_hash) AS formula_version_count,
       MIN(formula_hash) AS formula_hash, MIN(formula_text) AS formula_text
FROM sda_dev.mad_data_lab.formula_versions
WHERE case_id = 'CASE_0042'
GROUP BY case_id;
