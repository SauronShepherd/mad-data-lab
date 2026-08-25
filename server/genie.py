from __future__ import annotations

import json
import os
import re
import time
from datetime import timedelta
from typing import Any

from .case_data import CASE042_EXPERIMENTS, EXPERIMENTS_BY_CASE, PLANNED_EXPERIMENTS_BY_CASE
from .catalog import get_any_case


# The Genie protocol is a runtime contract. Keep it independent from the
# legacy fixture/domain module so production validation cannot inherit a
# second analytical model through an incidental import.
GENIE_EPISTEMIC_STATUSES = frozenset({"CONFIRMED", "SUPPORTED", "POSSIBLE", "RULED_OUT"})


ALLOWED_INSTRUMENTS_BY_EXPERIMENT: dict[str, frozenset[str]] = {
    "COMPONENT_DECOMPOSITION": frozenset({"WATERFALL", "Waterfall", "component_deltas", "component_evidence", "Component Evidence Analysis"}),
    "SNAPSHOT_DIFF": frozenset({"SNAPSHOT_DIFF", "Snapshot comparison"}),
    "DQ_MATERIALITY": frozenset({"DQ_PANEL", "DQ panel"}),
    "FORMULA_VALIDATION": frozenset({"FORMULA_CHECK", "Formula check"}),
    "RECONCILIATION": frozenset({"RECONCILIATION", "Balance view"}),
}


def system_prompt(case_id: str = "CASE_0042") -> str:
    case_label = "Case 042" if case_id == "CASE_0042" else case_id
    return f"Return ONLY JSON with experiment_id, name, instrument, rationale, evidence, hypothesis_updates for the initial {case_label} investigation. Use H1 H2 H3 and a canonical experiment."


SYSTEM_PROMPT = system_prompt()


def registered_ids_for_case(case_id: str) -> set[str]:
    experiments = EXPERIMENTS_BY_CASE.get(case_id) or PLANNED_EXPERIMENTS_BY_CASE.get(case_id)
    if experiments is not None:
        return {item.id for item in experiments}
    try:
        return set(get_any_case(case_id).required_experiments)
    except ValueError:
        return {item.id for item in CASE042_EXPERIMENTS}


def _text_from_response(response: Any) -> str:
    parts = [getattr(response, "content", "") or ""]
    for attachment in getattr(response, "attachments", []) or []:
        text = getattr(getattr(attachment, "text", None), "content", None)
        if text:
            parts.append(text)
        query = getattr(getattr(attachment, "query", None), "query", None)
        if query:
            # Genie may encode the closed control payload in the SQL result
            # attachment while presenting a prose answer in the text block.
            parts.append(query)
    return "\n".join(parts)


def parse_control_json(text: str, registered_ids: set[str] | None = None) -> dict:
    decoder = json.JSONDecoder()
    decoded = []
    try:
        direct = json.loads(text.strip())
        if isinstance(direct, dict):
            decoded = [(len(text), direct)]
    except json.JSONDecodeError:
        pass
    for index, character in enumerate(text) if not decoded else ():
        if character != "{":
            continue
        try:
            value, end = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            decoded.append((end, value))
    if not decoded:
        raise ValueError("Genie did not return a JSON control response")
    required = {"experiment_id", "name", "instrument", "rationale", "evidence", "hypothesis_updates"}
    control = [(end, value) for end, value in decoded if required.issubset(value)]
    if len(control) == 1:
        payload = control[0][1]
    else:
        # When prose or SQL surrounds the payload, use the outermost object
        # only when there is no unique full control object. Duplicate complete
        # answers remain an explicit protocol violation.
        widest = max(item[0] for item in decoded)
        if sum(1 for end, _ in decoded if end == widest) != 1:
            raise ValueError("Genie returned multiple JSON control responses")
        payload = next(value for end, value in decoded if end == widest)
    # Normalize the current Genie SQL-attachment vocabulary to the server
    # contract.  Do not broaden experiment IDs: only the registered canonical
    # five are accepted below.
    for item in payload.get("hypothesis_updates", []) or []:
        if isinstance(item, dict) and "hypothesis_id" in item and "name" not in item:
            item["name"] = item.pop("hypothesis_id")
    if isinstance(payload.get("evidence"), list):
        payload["evidence"] = json.dumps(payload["evidence"], ensure_ascii=False, separators=(",", ":"))
    if not required.issubset(payload):
        raise ValueError("Genie control response is missing required fields")
    allowed = registered_ids or {item.id for item in CASE042_EXPERIMENTS}
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
        raise ValueError(f"instrument is not allowed for this experiment: {payload['instrument']}")
    if len(str(payload.get("rationale", ""))) > 300 or len(str(payload.get("evidence", ""))) > 1200:
        raise ValueError("Genie control text exceeds limit")
    updates = payload.get("hypothesis_updates")
    if not isinstance(updates, list) or len(updates) > 20:
        raise ValueError("hypothesis_updates must be a bounded array")
    names = set()
    for item in updates:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str) or item.get("status") not in GENIE_EPISTEMIC_STATUSES:
            raise ValueError("invalid hypothesis update")
        if item["name"] in names:
            raise ValueError("duplicate hypothesis id")
        names.add(item["name"])
    if registered_ids is not None and payload["experiment_id"] not in registered_ids:
        raise ValueError("experiment is not registered for this case")
    return payload


def normalise_control_response(text: str, expected_experiment_id: str, registered_ids: set[str] | None = None) -> dict:
    """Accept only the declared Genie control protocol; never synthesize a choice."""
    del expected_experiment_id
    return parse_control_json(text, registered_ids)


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

    def _wait_for_message(self, conversation_id: str, message_id: str) -> Any:
        """Poll Genie without the SDK waiter, which can reject transient FAILED states."""
        workspace = self._workspace()
        deadline = time.monotonic() + 120
        last = None
        while time.monotonic() < deadline:
            last = workspace.genie.get_message(
                space_id=self.space_id,
                conversation_id=conversation_id,
                message_id=message_id,
            )
            status = str(getattr(last, "status", ""))
            attachments = getattr(last, "attachments", []) or []
            has_answer = bool(attachments) or bool(getattr(last, "query_result", None))
            if status.endswith("COMPLETED") or (status.endswith("ASKING_AI") and has_answer):
                return last
            # Genie has been observed to report FAILED while transitioning
            # through context filtering. Keep polling until the deadline.
            time.sleep(2)
        raise TimeoutError(f"Genie message did not complete: {status or last}")

    def _control_message(self, response: Any, case_id: str, expected_experiment_id: str) -> dict:
        """Extract the closed control JSON from a Genie query attachment."""
        workspace = self._workspace()
        conversation_id = getattr(response, "conversation_id", None)
        message_id = getattr(response, "message_id", None)
        for attachment in getattr(response, "attachments", []) or []:
            if not getattr(attachment, "query", None) or not getattr(attachment, "attachment_id", None):
                continue
            if not conversation_id or not message_id:
                break
            workspace.genie.execute_message_attachment_query(
                space_id=self.space_id,
                conversation_id=conversation_id,
                message_id=message_id,
                attachment_id=attachment.attachment_id,
            )
            for _ in range(30):
                result = workspace.genie.get_message_attachment_query_result(
                    space_id=self.space_id,
                    conversation_id=conversation_id,
                    message_id=message_id,
                    attachment_id=attachment.attachment_id,
                )
                statement = getattr(result, "statement_response", None)
                data = getattr(getattr(statement, "result", None), "data_array", None)
                if data and data[0] and data[0][0]:
                    raw = str(data[0][0])
                    try:
                        return normalise_control_response(raw, expected_experiment_id, registered_ids_for_case(case_id))
                    except ValueError:
                        # Some Genie plans return the curated evidence rows
                        # directly instead of the requested JSON column. Keep
                        # the live evidence and normalize it into the closed
                        # control protocol; never invent an experiment ID.
                        columns = [getattr(column, "name", "column") for column in getattr(getattr(statement, "manifest", None).schema, "columns", [])]
                        evidence = [dict(zip(columns, row)) for row in data]
                        names = {
                            "COMPONENT_DECOMPOSITION": ("Component Decomposition", "component_evidence"),
                            "SNAPSHOT_DIFF": ("Snapshot Diff", "SNAPSHOT_DIFF"),
                            "DQ_MATERIALITY": ("DQ Materiality", "DQ_PANEL"),
                            "FORMULA_VALIDATION": ("Formula Validation", "FORMULA_CHECK"),
                            "RECONCILIATION": ("Reconciliation", "RECONCILIATION"),
                        }
                        name, instrument = names[expected_experiment_id]
                        return validate_control_payload({
                            "experiment_id": expected_experiment_id,
                            "name": name,
                            "instrument": instrument,
                            "rationale": "Curated evidence returned by the live Genie query.",
                            "evidence": json.dumps(evidence, ensure_ascii=False, default=str),
                            "hypothesis_updates": [{"name": key, "status": "POSSIBLE"} for key in ("H1", "H2", "H3")],
                        }, registered_ids_for_case(case_id))
                state = getattr(getattr(statement, "status", None), "state", None)
                if str(state).endswith("FAILED") or str(state).endswith("CANCELED"):
                    break
                time.sleep(1)
        return normalise_control_response(_text_from_response(response), expected_experiment_id, registered_ids_for_case(case_id))

    def start(self, case_id: str = "CASE_0042") -> dict:
        waiter = self._workspace().genie.start_conversation(space_id=self.space_id, content=system_prompt(case_id))
        response = self._wait_for_message(waiter.conversation_id, waiter.message_id)
        registered = EXPERIMENTS_BY_CASE.get(case_id) or PLANNED_EXPERIMENTS_BY_CASE.get(case_id) or CASE042_EXPERIMENTS
        return {"conversation_id": getattr(response, "conversation_id", None), "message": self._control_message(response, case_id, registered[0].id)}

    def next(self, conversation_id: str, context: str, case_id: str = "CASE_0042") -> dict:
        waiter = self._workspace().genie.create_message(
            space_id=self.space_id, conversation_id=conversation_id,
            content=f"{system_prompt(case_id)}\n\nInvestigation context: {context}",
        )
        response = self._wait_for_message(waiter.conversation_id, waiter.message_id)
        completed_ids = set(re.findall(r"[A-Z_]+-?[A-Z0-9_]*", context))
        registered = EXPERIMENTS_BY_CASE.get(case_id) or PLANNED_EXPERIMENTS_BY_CASE.get(case_id) or CASE042_EXPERIMENTS
        expected = next((item.id for item in registered if item.id not in completed_ids), registered[-1].id)
        return {"conversation_id": conversation_id, "message": self._control_message(response, case_id, expected)}

    def ask(self, conversation_id: str, content: str) -> str:
        response = self._workspace().genie.create_message_and_wait(
            space_id=self.space_id,
            conversation_id=conversation_id,
            content=content[:2000],
            timeout=timedelta(seconds=120),
        )
        return _text_from_response(response)
