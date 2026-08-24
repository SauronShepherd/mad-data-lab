-- Canonical public/curated contract from the game specification.
-- No private truth table is granted to Genie resources.
CREATE SCHEMA IF NOT EXISTS mad_data_lab_public;
CREATE SCHEMA IF NOT EXISTS mad_data_lab_private;
CREATE SCHEMA IF NOT EXISTS mad_data_lab_curated;

CREATE TABLE IF NOT EXISTS mad_data_lab_public.case_definition (
  case_id STRING NOT NULL, public_number INT NOT NULL, slug STRING NOT NULL,
  generator_version INT NOT NULL, case_template_version INT NOT NULL,
  title STRING NOT NULL, hook STRING NOT NULL, datapoint_id STRING NOT NULL,
  entity_id STRING, period_id STRING, expected_value DECIMAL(18,2) NOT NULL,
  observed_value DECIMAL(18,2) NOT NULL, deviation DECIMAL(18,2) NOT NULL,
  currency STRING, scale STRING NOT NULL, difficulty STRING NOT NULL,
  release_state STRING NOT NULL, sort_order INT NOT NULL,
  required_case_ids STRING, learning_objectives STRING NOT NULL, status STRING NOT NULL
);
CREATE TABLE IF NOT EXISTS mad_data_lab_public.datapoint_result (
  case_id STRING NOT NULL, datapoint_id STRING NOT NULL, entity_id STRING,
  period_id STRING, run_id STRING NOT NULL, run_role STRING NOT NULL,
  value DECIMAL(18,2) NOT NULL, expected_value DECIMAL(18,2) NOT NULL,
  deviation DECIMAL(18,2) NOT NULL, formula_id STRING, formula_hash STRING,
  filter_id STRING, filter_hash STRING, population_hash STRING
);
CREATE TABLE IF NOT EXISTS mad_data_lab_public.calculation_trace (
  case_id STRING NOT NULL, datapoint_id STRING NOT NULL, run_id STRING NOT NULL,
  parent_node_id STRING, node_id STRING NOT NULL, node_type STRING NOT NULL,
  label STRING NOT NULL, operation STRING NOT NULL, formula STRING,
  value DECIMAL(18,2), previous_value DECIMAL(18,2), contribution_delta DECIMAL(18,2),
  source_table STRING, source_column STRING, filters_json STRING, join_json STRING,
  snapshot_id STRING, sequence_no INT NOT NULL
);
CREATE TABLE IF NOT EXISTS mad_data_lab_public.source_snapshot (
  snapshot_id STRING NOT NULL, case_id STRING NOT NULL, source_table STRING NOT NULL,
  status STRING NOT NULL, snapshot_role STRING NOT NULL, pipeline_run_id STRING
);
CREATE TABLE IF NOT EXISTS mad_data_lab_public.source_record (
  case_id STRING NOT NULL, snapshot_id STRING NOT NULL, business_key STRING NOT NULL,
  entity_id STRING, period_id STRING, component STRING, segment_id STRING,
  amount DECIMAL(18,2), record_status STRING NOT NULL, changed_from_previous BOOLEAN NOT NULL,
  duplicate_group_id STRING, included_by_filter BOOLEAN, source_table STRING NOT NULL,
  source_column STRING
);
CREATE TABLE IF NOT EXISTS mad_data_lab_public.snapshot_diff (
  case_id STRING NOT NULL, component STRING, business_key STRING NOT NULL,
  entity_id STRING, segment_id STRING, change_type STRING NOT NULL,
  old_value DECIMAL(18,2), new_value DECIMAL(18,2), impact DECIMAL(18,2) NOT NULL,
  duplicate_group_id STRING, pipeline_run_id STRING, previous_snapshot_id STRING,
  current_snapshot_id STRING NOT NULL
);
CREATE TABLE IF NOT EXISTS mad_data_lab_public.quality_issue (
  case_id STRING NOT NULL, issue_id STRING NOT NULL, rule_name STRING NOT NULL,
  severity STRING NOT NULL, affected_keys STRING, affected_row_count INT NOT NULL,
  estimated_impact DECIMAL(18,2), impact_is_overlapping BOOLEAN NOT NULL,
  status STRING NOT NULL, evidence_note STRING
);
CREATE TABLE IF NOT EXISTS mad_data_lab_public.pipeline_run_evidence (
  case_id STRING NOT NULL, pipeline_run_id STRING NOT NULL, source_snapshot_id STRING,
  execution_status STRING NOT NULL, replay_of_run_id STRING, note STRING
);
CREATE TABLE IF NOT EXISTS mad_data_lab_public.semantic_change_evidence (
  case_id STRING NOT NULL, semantic_type STRING NOT NULL, previous_id STRING,
  current_id STRING, previous_hash STRING, current_hash STRING,
  affected_population_count INT, estimated_impact DECIMAL(18,2), details_json STRING
);
CREATE TABLE IF NOT EXISTS mad_data_lab_public.technical_lineage_curated (
  case_id STRING NOT NULL, source_table STRING NOT NULL, source_column STRING,
  target_table STRING NOT NULL, target_column STRING, entity_type STRING NOT NULL,
  lineage_source STRING NOT NULL
);

-- Explicitly private and never included in resources/genie/*.json.
CREATE TABLE IF NOT EXISTS mad_data_lab_private.case_truth (
  case_id STRING NOT NULL, primary_component STRING, primary_source STRING,
  primary_cause STRING NOT NULL, secondary_cause STRING,
  affected_rows INT, expected_impact DECIMAL(18,2), secondary_expected_impact DECIMAL(18,2),
  expected_total_deviation DECIMAL(18,2) NOT NULL, confidence STRING NOT NULL,
  allowed_final_status_json STRING, expected_path_json STRING, truth_json STRING
);

CREATE OR REPLACE VIEW mad_data_lab_curated.snapshot_evidence AS
SELECT * FROM mad_data_lab_public.snapshot_diff;
CREATE OR REPLACE VIEW mad_data_lab_curated.quality_evidence AS
SELECT * FROM mad_data_lab_public.quality_issue;
CREATE OR REPLACE VIEW mad_data_lab_curated.semantic_evidence AS
SELECT * FROM mad_data_lab_public.semantic_change_evidence;
CREATE OR REPLACE VIEW mad_data_lab_curated.pipeline_evidence AS
SELECT * FROM mad_data_lab_public.pipeline_run_evidence;
CREATE OR REPLACE VIEW mad_data_lab_curated.lineage_evidence AS
SELECT * FROM mad_data_lab_public.technical_lineage_curated;
