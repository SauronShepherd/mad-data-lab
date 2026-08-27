from __future__ import annotations
from dataclasses import dataclass
from typing import Any

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
        super().__init__(self.message)

def envelope(error: AppError, request_id: str) -> dict[str, Any]:
    value: dict[str, Any] = {"code": error.code, "message": error.message, "retryable": error.retryable, "preserve_evidence": error.preserve_evidence, "request_id": request_id}
    if error.diagnostic_code: value["diagnostic_code"] = error.diagnostic_code
    if error.details: value["details"] = error.details
    return {"error": value}
