"""Validation and loading for the public, non-truth case catalog."""
from __future__ import annotations

from pathlib import Path
import re
from typing import Any

import yaml  # type: ignore[import-untyped]

from .models import Case


class CatalogError(ValueError):
    """Raised when the canonical public catalog violates its contract."""


_CASE_ID = re.compile(r"^CASE_\d{4}$")
_HYPOTHESIS_ID = re.compile(r"^H[1-8]$")
_EXPERIMENT_ID = re.compile(r"^[A-Z][A-Z0-9_]+$")
_REQUIRED = {
    "id", "number", "title", "metric", "state", "playable", "expected", "observed",
    "deviation", "hypotheses", "required_experiments",
}
_PRIVATE_MARKERS = ("case_truth", "primary_cause", "primary_component", "truth_json", "expected_path_json")


def load_catalog(path: str | Path | None = None) -> dict[str, Any]:
    """Load and validate the canonical catalog without exposing private truth."""
    catalog_path = Path(path) if path else Path(__file__).resolve().parents[2] / "cases/catalog.yaml"
    try:
        data = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise CatalogError(f"Unable to read catalog: {catalog_path}") from exc
    if not isinstance(data, dict) or data.get("version") != 1 or data.get("brand") != "MAD DATA LAB":
        raise CatalogError("catalog must declare version 1 and brand MAD DATA LAB")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise CatalogError("catalog cases must be a non-empty list")
    seen: set[str] = set()
    for case in cases:
        if not isinstance(case, dict) or set(case) != _REQUIRED:
            raise CatalogError("each catalog case must have exactly the canonical fields")
        case_id = case["id"]
        if not isinstance(case_id, str) or not _CASE_ID.fullmatch(case_id) or case_id in seen:
            raise CatalogError(f"invalid or duplicate case id: {case_id!r}")
        seen.add(case_id)
        serialized = yaml.safe_dump(case, sort_keys=True).lower()
        if any(marker in serialized for marker in _PRIVATE_MARKERS):
            raise CatalogError(f"private truth marker in public case: {case_id}")
        if not isinstance(case["number"], int) or f"CASE_{case['number']:04d}" != case_id:
            raise CatalogError(f"case number does not match id: {case_id}")
        if not isinstance(case["playable"], bool) or not isinstance(case["hypotheses"], list):
            raise CatalogError(f"invalid playability or hypotheses: {case_id}")
        if any(not isinstance(item, str) or not _HYPOTHESIS_ID.fullmatch(item) for item in case["hypotheses"]):
            raise CatalogError(f"invalid hypothesis id: {case_id}")
        experiments = case["required_experiments"]
        if not isinstance(experiments, list) or not experiments or any(
            not isinstance(item, str) or not _EXPERIMENT_ID.fullmatch(item) for item in experiments
        ):
            raise CatalogError(f"invalid required experiments: {case_id}")
        if case["playable"] != (case["state"] == "CORE"):
            raise CatalogError(f"playability must match CORE state: {case_id}")
    return data


def load_case_models(path: str | Path | None = None) -> list[Case]:
    """Return the canonical catalog as strict public domain objects."""
    return [Case.model_validate(item) for item in load_catalog(path)["cases"]]
