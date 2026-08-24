"""Live curated SQL gate for Case #042 through Databricks Statement Execution."""
from __future__ import annotations

import json
import os
from pathlib import Path

from databricks.sdk import WorkspaceClient

ROOT = Path(__file__).resolve().parents[1]


def query(client: WorkspaceClient, warehouse: str, sql: str) -> list[list[str]]:
    response = client.statement_execution.execute_statement(
        sql, warehouse, catalog="sda_dev", schema="mad_data_lab", wait_timeout="30s", row_limit=100
    )
    if response.status.state.value != "SUCCEEDED":
        raise RuntimeError(f"SQL failed: {response.status}")
    return response.result.data_array if response.result and response.result.data_array else []


def main() -> None:
    config = json.loads((ROOT / "resources/genie/case_0042.space.json").read_text(encoding="utf-8"))
    client = WorkspaceClient(profile=os.getenv("DATABRICKS_CONFIG_PROFILE", "sda"))
    warehouse = os.getenv("DATABRICKS_WAREHOUSE_ID", config["warehouse_id"])
    observation = query(client, warehouse, "SELECT expected_eur_m, observed_eur_m, deviation_eur_m FROM case_observations WHERE case_id = 'CASE_0042'")
    component = query(client, warehouse, "SELECT component_id, contribution_delta_eur_m FROM v_case042_experiment_decomposition ORDER BY ABS(contribution_delta_eur_m) DESC LIMIT 1")
    snapshot = query(client, warehouse, "SELECT SUM(net_impact_eur_m) FROM v_case042_snapshot_diff")
    formula = query(client, warehouse, "SELECT formula_version_count FROM v_case042_formula_check")
    dq = query(client, warehouse, "SELECT affected_rows, estimated_overlapping_impact_eur_m, overlaps_component_id FROM dq_signals WHERE case_id = 'CASE_0042'")
    assert observation and observation[0] == ["125.00", "118.20", "-6.80"], observation
    assert component and component[0][0] == "V2" and component[0][1] == "-5.90", component
    assert snapshot and snapshot[0][0] == "-5.90", snapshot
    assert formula and formula[0][0] == "1", formula
    assert dq and dq[0] == ["5", "-0.30", "V2"], dq
    print("live SQL gate: PASS (observation, decomposition, snapshot, formula, DQ overlap)")


if __name__ == "__main__":
    main()
