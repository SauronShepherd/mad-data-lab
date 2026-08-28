from __future__ import annotations
from dataclasses import dataclass
from typing import Any

ERROR_CODES = frozenset({
    "GENIE_NOT_CONFIGURED", "WAREHOUSE_NOT_CONFIGURED", "MISSING_ENVIRONMENT_VARIABLE",
    "GENIE_TIMEOUT", "GENIE_FAILED", "GENIE_MALFORMED_PROTOCOL", "GENIE_UNSUPPORTED_EXPERIMENT",
    "GENIE_QUERY_MISSING", "GENIE_QUERY_FAILED", "GENIE_EXPERIMENT_UNAVAILABLE", "GENIE_INVALID_EXPERIMENT", "CASE_NOT_FOUND", "EVIDENCE_SCHEMA_MISMATCH",
    "RECONCILIATION_FAILED", "DATA_INVARIANT_FAILED", "ILLEGAL_STATE_TRANSITION", "SESSION_NOT_FOUND",
    "DUPLICATE_ACTION", "WAREHOUSE_PENDING", "WAREHOUSE_QUOTA_EXHAUSTED", "APP_RESOURCE_UNAVAILABLE",
    "INVALID_REQUEST", "REQUEST_REJECTED", "SESSION_EXPIRED", "STATE_REVISION_CONFLICT",
    "GENIE_CIRCUIT_OPEN", "GENIE_EXPERIMENT_UNAVAILABLE", "COMPLETION_NOT_READY",
    "CROSS_CASE_EVIDENCE_FORBIDDEN", "FINAL_PREDICTION_NOT_YET_AVAILABLE",
    "FINAL_PREDICTION_REQUIRED", "INITIAL_PREDICTION_NOT_AVAILABLE",
    "HINT_NOT_YET_AVAILABLE", "INVALID_PREDICTION_ID", "VERDICT_INVALID",
    "GENIE_CONCLUSION_EMPTY", "GENIE_CONCLUSION_UNAVAILABLE", "SESSION_CAPACITY_REACHED", "UNHANDLED_REQUEST",
})

@dataclass
class AppError(Exception):
    code: str
    message: str
    status_code: int = 500
    retryable: bool = False
    preserve_evidence: bool = True
    diagnostic_code: str | None = None
    details: dict[str, Any] | None = None
    def __post_init__(self) -> None:
        if self.code not in ERROR_CODES:
            raise ValueError(f"unregistered application error code: {self.code}")
        super().__init__(self.message)

def envelope(error: AppError, request_id: str) -> dict[str, Any]:
    value: dict[str, Any] = {"code": error.code, "message": error.message, "retryable": error.retryable, "preserve_evidence": error.preserve_evidence, "request_id": request_id}
    if error.diagnostic_code: value["diagnostic_code"] = error.diagnostic_code
    if error.details: value["details"] = error.details
    return {"error": value}


_PUBLIC_MESSAGES = {
    "WAREHOUSE_PENDING": "The analytical warehouse is still starting.",
    "WAREHOUSE_QUOTA_EXHAUSTED": "The analytical warehouse is temporarily unavailable.",
    "APP_RESOURCE_UNAVAILABLE": "The application could not complete this request.",
}


def app_error_from_exception(exc: BaseException) -> AppError:
    """Convert adapter failures to the stable public taxonomy without leakage."""
    code = getattr(exc, "code", "APP_RESOURCE_UNAVAILABLE")
    if code not in ERROR_CODES:
        code = "APP_RESOURCE_UNAVAILABLE"
    retryable = code in {"WAREHOUSE_PENDING", "WAREHOUSE_QUOTA_EXHAUSTED", "APP_RESOURCE_UNAVAILABLE"}
    return AppError(code, _PUBLIC_MESSAGES.get(code, "The request could not be completed."), 503,
                    retryable=retryable, preserve_evidence=True, diagnostic_code=code)
