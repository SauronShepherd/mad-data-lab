from decimal import Decimal

import pytest

from backend.data.models import (
    ComponentResult,
    FormulaValidationResult,
    ObservationResult,
    ReconciliationResult,
    SnapshotGroup,
)


def test_sql_decimal_models_preserve_cent_precision_and_reject_unknown_columns():
    observation = ObservationResult.model_validate({
        'case_id':'CASE_0042','datapoint_id':'CAPITAL_AVAILABLE','entity_id':'PT001',
        'period_id':'2026-07','expected_value':'125.00','observed_value':'118.20',
        'deviation':'-6.80','formula_id':'CAPITAL_AVAILABLE_V1','formula_hash':'x',
    })
    assert observation.expected_value == Decimal('125.00')
    assert observation.deviation == Decimal('-6.80')
    with pytest.raises(ValueError):
        ObservationResult.model_validate({**observation.model_dump(), 'secret':'nope'})


def test_all_trusted_result_shapes_are_typed():
    assert ComponentResult(component='V2', previous_value='30.00', current_value='24.10', contribution_delta='-5.90').contribution_delta == Decimal('-5.90')
    assert SnapshotGroup(case_id='CASE_0042', component='V2', change_type='MODIFIED', record_count=23, total_impact='-5.20').total_impact == Decimal('-5.20')
    assert FormulaValidationResult(case_id='CASE_0042', previous_formula_id='F', current_formula_id='F', previous_formula_hash='a', current_formula_hash='a', formula_changed=False).formula_changed is False
    assert ReconciliationResult(case_id='CASE_0042', expected_deviation='-6.80', reconciled_deviation='-6.80', residual='0.00').residual == Decimal('0.00')
