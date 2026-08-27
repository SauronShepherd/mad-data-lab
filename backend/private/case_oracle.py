"""Narrow Case #042 scoring oracle; never serialized or sent to Genie."""
from __future__ import annotations

INITIAL_PREDICTION_IDS = frozenset({
    "PRED_SOURCE_VALUES_CHANGED",
    "PRED_DATA_QUALITY_PRIMARY",
    "PRED_FORMULA_CHANGED",
    "PRED_INSUFFICIENT_EVIDENCE",
})
FINAL_PREDICTION_IDS = frozenset({
    "FINAL_CHANGED_V2_SOURCE_RECORDS",
    "FINAL_DATA_QUALITY_PRIMARY",
    "FINAL_FORMULA_CHANGED",
    "FINAL_INSUFFICIENT_EVIDENCE",
})

def initial_prediction_correct(case_id: str, prediction_id: str) -> bool:
    return case_id == "CASE_0042" and prediction_id == "PRED_SOURCE_VALUES_CHANGED"

def final_prediction_correct(case_id: str, prediction_id: str) -> bool:
    return case_id == "CASE_0042" and prediction_id == "FINAL_CHANGED_V2_SOURCE_RECORDS"
