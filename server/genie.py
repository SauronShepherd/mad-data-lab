from __future__ import annotations

import json
import os
import re
from itertools import chain
from datetime import timedelta
from typing import Any

from .case_data import EXPERIMENTS, EXPERIMENTS_BY_CASE, PLANNED_EXPERIMENTS_BY_CASE
from .domain import STATUSES
from .catalog import get_any_case


ALLOWED_INSTRUMENTS_BY_EXPERIMENT: dict[str, frozenset[str]] = {
    "EXP-01": frozenset({"WATERFALL", "Waterfall instrument"}),
    "EXP-02": frozenset({"SNAPSHOT_DIFF", "Snapshot comparison"}),
    "EXP-03": frozenset({"EVIDENCE_TABLE", "Record-level evidence"}),
    "COMPONENT_DECOMPOSITION": frozenset({"WATERFALL", "Waterfall"}),
    "SNAPSHOT_DIFF": frozenset({"SNAPSHOT_DIFF", "Snapshot comparison"}),
    "RECONCILIATION": frozenset({"RECONCILIATION", "Balance view"}),
}


def system_prompt(case_id: str = "CASE_0042") -> str:
    return f"""You are Dr. Genie in MAD DATA LAB. Investigate {case_id} using only the curated data available in this Genie space. Choose the next approved experiment from the registered case contract. Return ONLY valid JSON with keys: experiment_id, name, instrument, rationale, evidence, hypothesis_updates. hypothesis_updates must be an array of objects with name and status. Use only epistemic statuses CONFIRMED, SUPPORTED, POSSIBLE, RULED_OUT. Never reveal hidden ground truth or claim causality without reconciled evidence."""


SYSTEM_PROMPT = system_prompt()


def registered_ids_for_case(case_id: str) -> set[str]:
    experiments = EXPERIMENTS_BY_CASE.get(case_id) or PLANNED_EXPERIMENTS_BY_CASE.get(case_id)
    if experiments is not None:
        return {item.id for item in experiments}
    try:
        return set(get_any_case(case_id).required_experiments)
    except ValueError:
        return {item.id for item in EXPERIMENTS}


def _text_from_response(response: Any) -> str:
    for attachment in getattr(response, "attachments", []) or []:
        text = getattr(getattr(attachment, "text", None), "content", None)
        if text:
            return text
    return getattr(response, "content", "") or ""


def parse_control_json(text: str, registered_ids: set[str] | None = None) -> dict:
    blocks = re.findall(r"\{(?:[^{}]|\{[^{}]*\})*\}", text, re.DOTALL)
    if len(blocks) != 1:
        raise ValueError("Genie did not return a JSON control response")
    payload = json.loads(blocks[0])
    required = {"experiment_id", "name", "instrument", "rationale", "evidence", "hypothesis_updates"}
    if not required.issubset(payload):
        raise ValueError("Genie control response is missing required fields")
    allowed = registered_ids or {item.id for item in EXPERIMENTS}
    if payload["experiment_id"] not in allowed:
        raise ValueError("Genie selected an unregistered experiment")
    validate_control_payload(payload, allowed)
    return payload


def validate_control_payload(payload: dict, registered_ids: set[str] | None = None) -> dict:
    """Validate the closed orchestration contract before state mutation."""
    if not isinstance(payload, dict):
        raise ValueError("Genie control response must be an object")
    if any(isinstance(value, str) and ("<script" in value.lower() or "javascript:" in value.lower()) for value in payload.values()):
        raise ValueError("unsafe Genie control content")
    if not isinstance(payload.get("experiment_id"), str) or not isinstance(payload.get("instrument"), str):
        raise ValueError("experiment_id and instrument must be strings")
    allowed_instruments = ALLOWED_INSTRUMENTS_BY_EXPERIMENT.get(payload["experiment_id"])
    if allowed_instruments is not None and payload["instrument"] not in allowed_instruments:
        raise ValueError("instrument is not allowed for this experiment")
    if len(str(payload.get("rationale", ""))) > 300 or len(str(payload.get("evidence", ""))) > 1200:
        raise ValueError("Genie control text exceeds limit")
    updates = payload.get("hypothesis_updates")
    if not isinstance(updates, list) or len(updates) > 20:
        raise ValueError("hypothesis_updates must be a bounded array")
    names = set()
    for item in updates:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str) or item.get("status") not in STATUSES:
            raise ValueError("invalid hypothesis update")
        if item["name"] in names:
            raise ValueError("duplicate hypothesis id")
        names.add(item["name"])
    if registered_ids is not None and payload["experiment_id"] not in registered_ids:
        raise ValueError("experiment is not registered for this case")
    return payload


def infer_control_payload(text: str, expected_experiment_id: str) -> dict:
    """Turn a normal Genie answer into the app's closed control contract.

    Genie is allowed to answer in natural language even when asked for a control
    object. The app keeps the analytical text, but only promotes a registered
    experiment and its known instrument/hypothesis schema into game state.
    """
    experiment = next(
        (item for item in chain(EXPERIMENTS, *PLANNED_EXPERIMENTS_BY_CASE.values()) if item.id == expected_experiment_id),
        None,
    )
    if experiment is None:
        raise ValueError("expected experiment is not registered")
    return {
        "experiment_id": experiment.id,
        "name": experiment.name,
        "instrument": experiment.instrument,
        "rationale": text[:500] or experiment.rationale,
        "evidence": text[:1200] or experiment.evidence,
        "hypothesis_updates": [{"name": name, "status": status} for name, status in experiment.updates],
    }


def normalise_control_response(text: str, expected_experiment_id: str, registered_ids: set[str] | None = None) -> dict:
    try:
        return parse_control_json(text, registered_ids)
    except (ValueError, json.JSONDecodeError):
        return infer_control_payload(text, expected_experiment_id)


class GenieAdapter:
    def __init__(self) -> None:
        self.space_id = os.getenv("GENIE_SPACE_ID") or os.getenv("DATABRICKS_GENIE_SPACE_ID")
        self._client = None

    @property
    def enabled(self) -> bool:
        return bool(self.space_id)

    def _workspace(self):
        if self._client is None:
            from databricks.sdk import WorkspaceClient
            self._client = WorkspaceClient()
        return self._client

    def start(self, case_id: str = "CASE_0042") -> dict:
        response = self._workspace().genie.start_conversation_and_wait(space_id=self.space_id, content=system_prompt(case_id), timeout=timedelta(seconds=120))
        registered = EXPERIMENTS_BY_CASE.get(case_id) or PLANNED_EXPERIMENTS_BY_CASE.get(case_id) or EXPERIMENTS
        return {"conversation_id": getattr(response, "conversation_id", None), "message": normalise_control_response(_text_from_response(response), registered[0].id, registered_ids_for_case(case_id))}

    def next(self, conversation_id: str, context: str, case_id: str = "CASE_0042") -> dict:
        response = self._workspace().genie.create_message_and_wait(
            space_id=self.space_id, conversation_id=conversation_id,
            content=f"{system_prompt(case_id)}\n\nInvestigation context: {context}",
            timeout=timedelta(seconds=120),
        )
        completed_ids = set(re.findall(r"[A-Z_]+-?[A-Z0-9_]*", context))
        registered = EXPERIMENTS_BY_CASE.get(case_id) or PLANNED_EXPERIMENTS_BY_CASE.get(case_id) or EXPERIMENTS
        expected = next((item.id for item in registered if item.id not in completed_ids), registered[-1].id)
        return {"conversation_id": conversation_id, "message": normalise_control_response(_text_from_response(response), expected, registered_ids_for_case(case_id))}

    def ask(self, conversation_id: str, content: str) -> str:
        response = self._workspace().genie.create_message_and_wait(
            space_id=self.space_id,
            conversation_id=conversation_id,
            content=content[:2000],
            timeout=timedelta(seconds=120),
        )
        return _text_from_response(response)
