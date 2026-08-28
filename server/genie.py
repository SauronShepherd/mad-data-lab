from __future__ import annotations

import json
import re
import time
from datetime import timedelta
from typing import Any

from .case_data import CASE042_EXPERIMENTS, EXPERIMENTS_BY_CASE, PLANNED_EXPERIMENTS_BY_CASE
from .catalog import DEFAULT_CASE_ID, get_any_case
from .config import load_settings
from backend.genie.protocol import validate_control_response


class CircuitOpenError(RuntimeError):
    """Raised when a session has exceeded its consecutive live-failure budget."""


class SessionCircuitBreaker:
    """Small in-memory breaker; state is scoped to one session by the caller."""
    def __init__(self, threshold: int = 3) -> None:
        self.threshold = threshold
        self.consecutive_failures = 0
        self.open = False

    def before_request(self) -> None:
        if self.open:
            raise CircuitOpenError("Genie recovery is required for this session")

    def record_success(self) -> None:
        self.consecutive_failures = 0
        self.open = False

    def record_failure(self) -> None:
        self.consecutive_failures += 1
        if self.consecutive_failures >= self.threshold:
            self.open = True


# The Genie protocol is a runtime contract. Keep it independent from the
# legacy fixture/domain module so production validation cannot inherit a
# second analytical model through an incidental import.
GENIE_EPISTEMIC_STATUSES = frozenset({"CONFIRMED", "SUPPORTED", "POSSIBLE", "RULED_OUT"})


ALLOWED_INSTRUMENTS_BY_EXPERIMENT: dict[str, frozenset[str]] = {
    "COMPONENT_DECOMPOSITION": frozenset({"WATERFALL", "Waterfall", "component_deltas", "component_evidence", "Component Evidence Analysis", "Component Evidence Table"}),
    "SNAPSHOT_DIFF": frozenset({"SNAPSHOT_DIFF", "Snapshot comparison", "snapshot_evidence"}),
    "DQ_MATERIALITY": frozenset({"DQ_PANEL", "DQ panel", "quality_evidence"}),
    "FORMULA_VALIDATION": frozenset({"FORMULA_CHECK", "Formula check", "semantic_evidence"}),
    "RECONCILIATION": frozenset({"RECONCILIATION", "Balance view", "case_summary"}),
}


def system_prompt(case_id: str = DEFAULT_CASE_ID) -> str:
    case_label = "Case 042" if case_id == "CASE_0042" else case_id
    return (
        f"For the {case_label} investigation, return exactly one MAD DATA LAB schema_version 1.0 JSON object. "
        "Use hypotheses with IDs H1, H2, H3 and statuses CONFIRMED, SUPPORTED, POSSIBLE, or RULED_OUT. "
        "For RUN_EXPERIMENT, include selected_experiment {id, question, target_component} and instrument {id, title}; "
        "choose only a currently allowed registered Experiment/Instrument and never use hidden truth or arbitrary SQL. "
        "Set target_component to null for every Experiment except SNAPSHOT_DIFF; for SNAPSHOT_DIFF use exactly one of V1, V2, V3, or V4. "
        "Include observation, next_action, and a concise scientist_line. Do not return multiple JSON objects. "
        "Begin the investigation now: return the first control object for the registered experiment that best tests the leading hypothesis."
    )


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


def parse_control_json(text: str, registered_ids: set[str] | None = None, expected_experiment_id: str | None = None) -> dict:
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
    control_keys = required - {"hypothesis_updates"}
    control = [(end, value) for end, value in decoded if control_keys.issubset(value)]
    # ``expected_experiment_id`` is retained as a compatibility parameter for
    # callers from the retired prototype, but it is deliberately not used as
    # a golden-answer constraint. The server validates membership in the
    # current allowed set below; any legal selection is acceptable.
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


def normalise_control_response(text: str, expected_experiment_id: str | None = None, registered_ids: set[str] | None = None) -> dict:
    """Accept a registered Genie choice without imposing a golden sequence."""
    return parse_control_json(text, registered_ids, expected_experiment_id)


class GenieAdapter:
    def __init__(self, *, clock=time.monotonic, sleeper=time.sleep) -> None:
        self.space_id = load_settings().genie_space_id
        self._client = None
        self._clock = clock
        self._sleeper = sleeper

    def _transient_call(self, operation, *, attempts: int = 2):
        """Retry only transport-like failures, never a completed mutation."""
        last_error = None
        for attempt in range(attempts):
            try:
                return operation()
            except (TimeoutError, ConnectionError, OSError) as exc:
                last_error = exc
                if attempt + 1 < attempts:
                    self._sleeper(0.05 * (attempt + 1))
        raise last_error  # type: ignore[misc]

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
        settings = load_settings()
        deadline = self._clock() + settings.genie_request_timeout_seconds
        last = None
        while self._clock() < deadline:
            last = workspace.genie.get_message(
                space_id=self.space_id,
                conversation_id=conversation_id,
                message_id=message_id,
            )
            status = str(getattr(last, "status", ""))
            attachments = getattr(last, "attachments", []) or []
            # A query attachment is an intermediate plan. Only a query result
            # or text attachment is sufficient to treat ASKING_AI as answered.
            has_answer = bool(getattr(last, "query_result", None)) or any(
                getattr(attachment, "text", None) is not None for attachment in attachments
            )
            if status.endswith("COMPLETED") or (status.endswith("ASKING_AI") and has_answer):
                return last
            if status.endswith("FAILED"):
                raise RuntimeError("Genie message failed")
            if status.endswith("CANCELED") or status.endswith("CANCELLED"):
                raise RuntimeError("Genie message was canceled")
            self._sleeper(max(0.05, settings.genie_poll_interval_ms / 1000))
        raise TimeoutError(f"Genie message did not complete: {status or last}")

    def _control_message(self, response: Any, case_id: str, allowed_experiments: set[str]) -> dict:
        """Extract the closed control JSON from a Genie query attachment."""
        workspace = self._workspace()
        conversation_id = getattr(response, "conversation_id", None)
        message_id = getattr(response, "message_id", None)
        # The live boundary accepts only the V3 control object. Legacy
        # fixture-space payloads are intentionally not a production fallback.
        # ``response.content`` is the prompt sent to Genie, not an answer.
        # It contains the schema marker by design, so inspecting it would
        # misclassify every live turn as a V3 response and bypass managed
        # attachment handling.
        answer_parts: list[str] = []
        query_result = getattr(response, "query_result", None)
        statement = getattr(query_result, "statement_response", query_result)
        rows = getattr(getattr(statement, "result", None), "data_array", None) or []
        for row in rows:
            if row:
                answer_parts.append(str(row[0]))
        for answer_attachment in getattr(response, "attachments", []) or []:
            answer_text = getattr(getattr(answer_attachment, "text", None), "content", None)
            if answer_text:
                answer_parts.append(str(answer_text))
            answer_query = getattr(getattr(answer_attachment, "query", None), "query", None)
            if answer_query:
                answer_parts.append(str(answer_query))
        v3_text = "\n".join(answer_parts)
        if not v3_text:
            candidate_content = str(getattr(response, "content", "") or "").strip()
            if candidate_content.startswith("{") or candidate_content.startswith("```json"):
                v3_text = candidate_content
        if "schema_version" in v3_text:
            try:
                v3 = validate_control_response(
                    v3_text,
                    active_case_id=case_id,
                    allowed_experiments=registered_ids_for_case(case_id),
                    instrument_for_experiment=lambda experiment: {
                        "COMPONENT_DECOMPOSITION": {"WATERFALL"},
                        "SNAPSHOT_DIFF": {"SNAPSHOT_DIFF"},
                        "DQ_MATERIALITY": {"DQ_PANEL"},
                        "FORMULA_VALIDATION": {"FORMULA_CHECK"},
                        "RECONCILIATION": {"RECONCILIATION"},
                    }.get(experiment, set()),
                    valid_targets=lambda experiment: {"V1", "V2", "V3", "V4"} if experiment == "SNAPSHOT_DIFF" else set(),
                    allowed_hypothesis_ids={"H1", "H2", "H3"},
                )
                return v3.model_dump(mode="json") | {"message_id": message_id, "conversation_id": conversation_id, "source": "genie"}
            except (TypeError, ValueError) as exc:
                raise ValueError(f"invalid V3 Genie control response: {exc}") from exc
        raise ValueError("Genie answer did not contain a valid V3 control payload")

    def start(self, case_id: str = DEFAULT_CASE_ID) -> dict:
        registered = EXPERIMENTS_BY_CASE.get(case_id) or PLANNED_EXPERIMENTS_BY_CASE.get(case_id) or CASE042_EXPERIMENTS
        allowed = {item.id for item in registered}
        last_error = None
        conversation_id = None
        # One original response plus exactly one protocol repair attempt.
        for _ in range(2):
            if _ == 0:
                waiter = self._workspace().genie.start_conversation(space_id=self.space_id, content=system_prompt(case_id))
            else:
                # Repair the same conversation so Genie can see the invalid
                # response and correct its protocol, rather than restarting
                # from an identical prompt in a fresh conversation.
                waiter = self._workspace().genie.create_message(
                    space_id=self.space_id,
                    conversation_id=conversation_id,
                    content=(
                        "Protocol repair: your previous response was invalid. "
                        "Return exactly one JSON control object now, with no SQL, "
                        "prose, Markdown, or query attachments. Include experiment_id, "
                        "name, instrument, rationale, evidence, and hypothesis_updates. "
                        "Set target_component to null unless experiment_id is SNAPSHOT_DIFF; then use exactly V1, V2, V3, or V4."
                    ),
                )
            response = self._wait_for_message(waiter.conversation_id, waiter.message_id)
            conversation_id = getattr(response, "conversation_id", None) or waiter.conversation_id
            try:
                return {"conversation_id": getattr(response, "conversation_id", None), "message": self._control_message(response, case_id, allowed)}
            except ValueError as exc:
                last_error = exc
        raise ValueError("Genie did not produce a valid initial control response after retries") from last_error

    def next(self, conversation_id: str, context: str, case_id: str = DEFAULT_CASE_ID) -> dict:
        completed_ids = set(re.findall(r"[A-Z_]+-?[A-Z0-9_]*", context))
        registered = EXPERIMENTS_BY_CASE.get(case_id) or PLANNED_EXPERIMENTS_BY_CASE.get(case_id) or CASE042_EXPERIMENTS
        allowed = {item.id for item in registered if item.id not in completed_ids}
        if not allowed:
            raise ValueError("no registered Experiments remain")
        last_error = None
        for _ in range(2):
            waiter = self._workspace().genie.create_message(
                space_id=self.space_id, conversation_id=conversation_id,
                content=f"{system_prompt(case_id)}\n\nInvestigation context: {context}",
            )
            response = self._wait_for_message(waiter.conversation_id, waiter.message_id)
            try:
                message = self._control_message(response, case_id, allowed)
                # The canonical V3 protocol nests the selection, while the
                # session ledger consumes the bounded flattened experiment
                # DTO. Normalize at this boundary so live and fixture paths
                # share one state-mutation shape.
                selected = message.get("selected_experiment") or {}
                instrument = message.get("instrument") or {}
                if selected.get("id"):
                    message = message | {
                        "experiment_id": selected["id"],
                        "name": selected.get("question") or selected["id"],
                        "instrument": instrument.get("id"),
                        "rationale": message.get("scientist_line", ""),
                    }
                return {"conversation_id": conversation_id, "message": message}
            except ValueError as exc:
                last_error = exc
        raise ValueError("Genie did not produce a valid experiment response after retries") from last_error

    def ask(self, conversation_id: str, content: str) -> str:
        response = self._transient_call(lambda: self._workspace().genie.create_message_and_wait(
            space_id=self.space_id,
            conversation_id=conversation_id,
            content=content[:2000],
            timeout=timedelta(seconds=load_settings().genie_request_timeout_seconds),
        ))
        return _text_from_response(response)
