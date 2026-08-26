from __future__ import annotations

import logging
import os
import time
from threading import RLock
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .case_data import EXPERIMENTS_BY_CASE, PLANNED_EXPERIMENTS_BY_CASE, experiment_payload
from .catalog import DEFAULT_CASE_ID, FULL_CASE_CATALOG, case_availability, get_any_case
from .genie import GenieAdapter
from backend.genie.decisions import allowed_set_digest
from backend.genie.client import CanonicalGenieBoundary
from .state import InvestigationState, transition
from backend.data.repositories import EvidenceRepository
from .config import load_settings


app = FastAPI(title="MAD DATA LAB API", version="0.1.0")
LOGGER = logging.getLogger("mad_data_lab")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = uuid.uuid4().hex
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
genie = CanonicalGenieBoundary(GenieAdapter())
evidence_repository = EvidenceRepository()
SESSIONS: dict[str, dict] = {}
SESSION_MUTATION_LOCK = RLock()
PROGRESSION: dict[str, Any] = {"completed_case_ids": set(), "best_scores": {}}

# Canonical V3 shell states for the documented session API. The older
# /api/investigations route retains its compatibility protocol separately.
CASE_CATALOG_STATE = "CASE_CATALOG"
CASE_BRIEFING_STATE = "CASE_BRIEFING"
STARTING_INVESTIGATION_STATE = "STARTING_INVESTIGATION"
HYPOTHESES_READY_STATE = "HYPOTHESES_READY"
# The Case contract is deliberately identifier-based.  Never let free-form
# Genie text reintroduce the retired prototype hypothesis names.
CANONICAL_HYPOTHESES = (
    {"name": "H1", "status": "POSSIBLE"},
    {"name": "H2", "status": "POSSIBLE"},
    {"name": "H3", "status": "POSSIBLE"},
)
SELECTING_EXPERIMENT_STATE = "SELECTING_EXPERIMENT"
RUNNING_EXPERIMENT_STATE = "RUNNING_EXPERIMENT"
EXPERIMENT_RESULT_STATE = "EXPERIMENT_RESULT"
EVIDENCE_EXPLORATION_STATE = "EVIDENCE_EXPLORATION"
PLAYER_PREDICTION_FINAL_STATE = "PLAYER_PREDICTION_FINAL"
CONCLUDING_STATE = "CONCLUDING"
DEBRIEF_STATE = "DEBRIEF"


def fixture_mode_enabled() -> bool:
    """Allow offline fixture play only when explicitly enabled for local use."""
    return load_settings().allow_fixture_mode


def review_mode_enabled() -> bool:
    return load_settings().challenge_review_mode


def observation_payload(case) -> dict[str, Any]:
    return {
        "case_id": case.id,
        "title": case.title,
        "datapoint_id": case.metric.upper().replace(" ", "_"),
        "entity_id": "PT001",
        "period_id": "2026-07",
        "expected": case.expected,
        "observed": case.observed,
        "deviation": case.deviation,
        "unit": "EUR_M",
        "currency": "EUR",
        "scale": "MILLIONS",
    }


def append_event(session: dict, event_type: str, **payload: Any) -> None:
    events = session.setdefault("events", [])
    events.append({"sequence": len(events) + 1, "type": event_type, **payload})


def persist_pending_decision(session: dict, message: dict[str, Any], registered: tuple) -> None:
    """Persist a valid start selection without marking it as completed evidence.

    Legacy spaces return the older control shape and therefore do not create a
    pending decision. New V3 protocol responses use ``selected_experiment``.
    """
    selected = message.get("selected_experiment")
    instrument = message.get("instrument")
    if not isinstance(selected, dict) or not isinstance(instrument, dict):
        return
    experiment_id = selected.get("id")
    instrument_id = instrument.get("id")
    allowed = {item.id for item in registered}
    if experiment_id not in allowed or not instrument_id:
        return
    session["pending_decision"] = {
        "message_id": message.get("message_id"),
        "experiment_id": experiment_id,
        "instrument_id": instrument_id,
        "target": selected.get("target_component"),
        "allowed_set_digest": allowed_set_digest(allowed),
        "protocol_sha256": message.get("protocol_sha256"),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    append_event(session, "PENDING_EXPERIMENT", experiment_id=experiment_id, source="genie")



class StartInvestigationRequest(BaseModel):
    case_id: str = Field(default=DEFAULT_CASE_ID, pattern=r"^CASE_\d{4}$")


class ExperimentRequest(BaseModel):
    case_id: str = Field(pattern=r"^CASE_\d{4}$")
    completed_experiments: list[str] = Field(default_factory=list)
    player_prediction: str | None = None
    conversation_id: str | None = None


class GenieQuestionRequest(BaseModel):
    case_id: str = Field(pattern=r"^CASE_\d{4}$")
    conversation_id: str | None = None
    question: str = Field(min_length=1, max_length=2000)


class SessionNextRequest(BaseModel):
    completed_experiments: list[str] = Field(default_factory=list)
    player_prediction: str | None = None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "genie_mode": "live" if genie.enabled else ("fixture" if fixture_mode_enabled() else "unavailable")}


@app.get("/api/cases")
def cases() -> dict:
    review_mode = review_mode_enabled()
    completed = PROGRESSION["completed_case_ids"]
    return {"cases": [case.public_payload() | {"availability": case_availability(case, review_mode=review_mode, completed_case_ids=completed)} for case in FULL_CASE_CATALOG]}


@app.get("/api/health")
def api_health() -> dict[str, str]:
    return health()


@app.get("/api/config")
def config() -> dict:
    review_mode = review_mode_enabled()
    enabled = [c.id for c in FULL_CASE_CATALOG if case_availability(c, review_mode=review_mode, completed_case_ids=PROGRESSION["completed_case_ids"]) == "AVAILABLE"]
    return {"protocol_version": "1.0", "fixture_mode": (not genie.enabled and fixture_mode_enabled()), "review_mode": review_mode, "enabled_cases": enabled}


@app.get("/api/progression")
def progression() -> dict:
    completed = sorted(PROGRESSION["completed_case_ids"])
    best_scores = dict(PROGRESSION["best_scores"])
    review_mode = review_mode_enabled()
    available = [c.id for c in FULL_CASE_CATALOG if case_availability(c, review_mode=review_mode, completed_case_ids=PROGRESSION["completed_case_ids"]) == "AVAILABLE"]
    return {"completed_case_ids": completed, "best_scores": best_scores, "available_case_ids": available}


@app.get("/api/cases/{case_id}/experiments")
def case_experiments(case_id: str) -> dict:
    try:
        case = get_any_case(case_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {
        "case_id": case.id,
        "state": case.state,
        "experiments": list(case.required_experiments),
        "ready": case.id in EXPERIMENTS_BY_CASE,
        "catalog": [experiment_payload(item, index, case.id) for index, item in enumerate(EXPERIMENTS_BY_CASE.get(case.id) or PLANNED_EXPERIMENTS_BY_CASE.get(case.id, ()))],
    }


@app.get("/api/cases/{case_id}")
def case_detail(case_id: str) -> dict:
    try:
        case = get_any_case(case_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"case": {"id": case.id, "number": f"{case.number:03d}", "title": case.title, "metric": case.metric, "hook": case.hook, "difficulty": case.difficulty, "state": case.state}}


@app.post("/api/investigations", status_code=201)
def start_investigation(request: StartInvestigationRequest) -> dict:
    try:
        case = get_any_case(request.case_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    review_mode = review_mode_enabled()
    if case_availability(case, review_mode=review_mode, completed_case_ids=PROGRESSION["completed_case_ids"]) != "AVAILABLE":
        raise HTTPException(status_code=409, detail="This Case is not enabled yet")
    if not genie.enabled and not fixture_mode_enabled():
        raise HTTPException(status_code=503, detail="Live Genie is unavailable")
    registered_experiments = EXPERIMENTS_BY_CASE.get(request.case_id) or PLANNED_EXPERIMENTS_BY_CASE.get(request.case_id, ())
    if genie.enabled:
        try:
            live = genie.start(request.case_id)
            session_id = str(uuid.uuid4())
            SESSIONS[session_id] = {"case_id": request.case_id, "completed": [], "evidence_entitlements": [], "events": [], "state": InvestigationState.BRIEFING.value, "created_at": datetime.now(timezone.utc).isoformat(), "score": 0, "score_events": ["START_INVESTIGATION"], "conversation_id": live["conversation_id"], "diagnostic_id": uuid.uuid4().hex}
            return {"investigation_id": session_id, "session_id": session_id, "conversation_id": live["conversation_id"], "case_id": request.case_id, "observation": observation_payload(case), "hypotheses": [name for name, _ in registered_experiments[0].updates] if registered_experiments else [], "source": "genie"}
        except Exception as exc:
            # A configured live Genie is authoritative.  Do not silently turn
            # an outage into a scripted analytical session.
            raise HTTPException(status_code=503, detail="Live Genie is unavailable") from exc
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = {"case_id": request.case_id, "completed": [], "evidence_entitlements": [], "events": [], "state": InvestigationState.BRIEFING.value, "created_at": datetime.now(timezone.utc).isoformat(), "score": 0, "score_events": ["START_INVESTIGATION"], "diagnostic_id": uuid.uuid4().hex}
    return {
        "investigation_id": session_id,
        "session_id": session_id,
        "case_id": request.case_id,
        "observation": observation_payload(case),
        "hypotheses": [name for name, _ in registered_experiments[0].updates] if registered_experiments else [],
    }


@app.post("/api/sessions", status_code=201)
def create_session(request: StartInvestigationRequest) -> dict:
    try:
        case = get_any_case(request.case_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    review_mode = review_mode_enabled()
    if case_availability(case, review_mode=review_mode, completed_case_ids=PROGRESSION["completed_case_ids"]) != "AVAILABLE":
        raise HTTPException(status_code=409, detail="This Case is not enabled yet")
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = {"case_id": request.case_id, "completed": [], "evidence_entitlements": [], "events": [], "state": CASE_BRIEFING_STATE, "created_at": datetime.now(timezone.utc).isoformat(), "score": 0, "score_events": [], "diagnostic_id": uuid.uuid4().hex}
    append_event(SESSIONS[session_id], "STATE", from_state=CASE_CATALOG_STATE, to_state=CASE_BRIEFING_STATE)
    return {"session_id": session_id, "case_id": request.case_id, "state": CASE_BRIEFING_STATE, "score": 0}


@app.post("/api/sessions/{session_id}/start")
def session_start(session_id: str) -> dict:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Investigation not found")
    # A failed live turn is retryable: no Experiment/evidence is committed,
    # so a client retry must be allowed to re-enter the Genie boundary.
    retryable_states = {CASE_BRIEFING_STATE, "WAITING_FOR_GENIE"}
    if session["state"] not in retryable_states:
        raise HTTPException(status_code=409, detail="Investigation has already started")
    previous = session["state"]
    session["state"] = STARTING_INVESTIGATION_STATE
    append_event(session, "STATE", from_state=previous, to_state=session["state"])
    registered = EXPERIMENTS_BY_CASE.get(session["case_id"]) or PLANNED_EXPERIMENTS_BY_CASE.get(session["case_id"], ())
    conversation_id = None
    source = "fixture"
    hypotheses = [dict(item) for item in CANONICAL_HYPOTHESES]
    if genie.enabled:
        try:
            live = genie.start(session["case_id"])
            conversation_id = live["conversation_id"]
            # The live space may contain stale prose from an older iteration.
            # Preserve the live conversation, but expose only the current
            # contract's hypothesis IDs and valid epistemic statuses.
            live_updates = live["message"].get("hypothesis_updates", ())
            allowed = {item["name"] for item in CANONICAL_HYPOTHESES}
            statuses = {"CONFIRMED", "SUPPORTED", "POSSIBLE", "RULED_OUT"}
            if isinstance(live_updates, list):
                candidate = [
                    {"name": str(item.get("name")), "status": str(item.get("status"))}
                    for item in live_updates
                    if isinstance(item, dict)
                    and item.get("name") in allowed
                    and item.get("status") in statuses
                ]
                if candidate:
                    by_name = {item["name"]: item for item in candidate}
                    hypotheses = [by_name.get(item["name"], item) for item in CANONICAL_HYPOTHESES]
            persist_pending_decision(session, live["message"], registered)
            source = "genie"
        except Exception as exc:
            LOGGER.exception("live Genie start failed")
            session["state"] = "WAITING_FOR_GENIE"
            append_event(session, "STATE", from_state=STARTING_INVESTIGATION_STATE, to_state=session["state"])
            raise HTTPException(status_code=503, detail="Live Genie is unavailable") from exc
    elif not fixture_mode_enabled():
        session["state"] = "WAITING_FOR_GENIE"
        append_event(session, "STATE", from_state=STARTING_INVESTIGATION_STATE, to_state=session["state"])
        raise HTTPException(status_code=503, detail="Live Genie is unavailable")
    session["conversation_id"] = conversation_id
    session["state"] = HYPOTHESES_READY_STATE
    session["score_events"].append("START_INVESTIGATION")
    append_event(session, "STATE", from_state=STARTING_INVESTIGATION_STATE, to_state=session["state"], source=source)
    return {"session_id": session_id, "case_id": session["case_id"], "status": "IN_PROGRESS", "state": session["state"], "conversation_id": conversation_id, "observation": observation_payload(get_any_case(session["case_id"])), "hypotheses": hypotheses}


@app.get("/api/sessions/{session_id}")
def get_session(session_id: str) -> dict:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Investigation not found")
    return {"session_id": session_id, **session}


@app.post("/api/sessions/{session_id}/restart")
def restart_session(session_id: str) -> dict:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Investigation not found")
    case_id = session["case_id"]
    diagnostic_id = session.get("diagnostic_id", uuid.uuid4().hex)
    SESSIONS[session_id] = {"case_id": case_id, "completed": [], "evidence_entitlements": [], "events": [], "state": CASE_BRIEFING_STATE, "created_at": datetime.now(timezone.utc).isoformat(), "score": 0, "score_events": [], "diagnostic_id": diagnostic_id}
    append_event(SESSIONS[session_id], "RESTART", reason="USER_REQUESTED_RESTART")
    return {"session_id": session_id, "case_id": case_id, "state": CASE_BRIEFING_STATE, "diagnostic_id": diagnostic_id}


@app.get("/api/sessions/{session_id}/evidence")
def session_evidence(session_id: str, limit: int = Query(default=100, ge=1, le=100), offset: int = Query(default=0, ge=0), business_key: str | None = Query(default=None, max_length=64)) -> dict:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Investigation not found")
    if "SNAPSHOT_IMPACT" not in session.get("evidence_entitlements", []):
        raise HTTPException(status_code=409, detail="Snapshot evidence has not been earned")
    if not session.get("inspected_evidence"):
        session["inspected_evidence"] = True
        session["score"] = min(1000, session.get("score", 0) + 100)
        session.setdefault("score_events", []).append("INSPECT_HIGH_VALUE_EVIDENCE")
        append_event(session, "EVIDENCE_INSPECTED", evidence_scope="CURATED_SOURCE_RECORDS")
        session["state"] = EVIDENCE_EXPLORATION_STATE
    if session["case_id"] == "CASE_0042":
        evidence = []
        for item in evidence_repository.records(session["case_id"], limit=100, business_key=business_key):
            payload = item.model_dump()
            for key in ("old_value", "new_value", "impact"):
                if payload[key] is not None:
                    payload[key] = float(payload[key])
            evidence.append(payload)
    else:
        raise HTTPException(status_code=409, detail="Curated evidence is not available for this Case")
    return {"session_id": session_id, "case_id": session["case_id"], "total": len(evidence), "offset": offset, "limit": limit, "evidence": evidence[offset:offset + limit]}


@app.post("/api/sessions/{session_id}/prediction")
def session_prediction(session_id: str, request: dict) -> dict:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Investigation not found")
    prediction = str(request.get("prediction", ""))[:200]
    if not session.get("prediction") and prediction:
        session["score"] = min(1000, session.get("score", 0) + 50)
        session.setdefault("score_events", []).append("FIRST_PREDICTION")
        if session["case_id"] == "CASE_0042" and "component" in prediction.lower():
            session["score"] = min(1000, session["score"] + 100)
            session.setdefault("score_events", []).append("CORRECT_INITIAL_PREDICTION")
    session["prediction"] = prediction
    append_event(session, "PREDICTION", prediction=prediction)
    return {"accepted": True, "prediction": session["prediction"]}


@app.post("/api/sessions/{session_id}/hint")
def session_hint(session_id: str) -> dict:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Investigation not found")
    hints_used = session.get("hints", 0)
    if hints_used >= 3:
        raise HTTPException(status_code=409, detail="All hints have been used")
    hints = {
        "CASE_0042": (
            "Look for the component with the largest absolute contribution.",
            "V2 explains most of the deviation. What changed underneath it?",
            "Compare the V2 source snapshot and reconcile its record-level impact.",
        ),
    }
    case_hints = hints.get(session["case_id"], ("Test the strongest available signal.", "Inspect the supporting evidence.", "Reconcile the full deviation."))
    session["hints"] = hints_used + 1
    session["score"] = max(0, session.get("score", 0) - 50)
    session.setdefault("score_events", []).append("HINT")
    append_event(session, "HINT", hint_number=session["hints"])
    return {"hint_number": session["hints"], "hint": case_hints[hints_used]}


@app.post("/api/sessions/{session_id}/conclude")
def conclude_session(session_id: str) -> dict:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Investigation not found")
    required = len(EXPERIMENTS_BY_CASE.get(session["case_id"]) or PLANNED_EXPERIMENTS_BY_CASE.get(session["case_id"], ()))
    if len(session.get("completed", [])) < required:
        raise HTTPException(status_code=409, detail="Required evidence is incomplete")
    session["status"] = "COMPLETE"
    previous = session["state"]
    session["state"] = CONCLUDING_STATE
    append_event(session, "STATE", from_state=previous, to_state=session["state"])
    previous = session["state"]
    session["state"] = DEBRIEF_STATE
    append_event(session, "STATE", from_state=previous, to_state=session["state"])
    score = session.get("score", 0)
    score += min(300, 100 * len(session.get("completed", [])))
    score += 125
    score = max(0, min(1000, score))
    session.setdefault("score_events", []).append("FINISH_DEBRIEF")
    badges = {"Data Apprentice"}
    if score >= 800:
        badges.add("Metric Scientist")
    if session.get("inspected_evidence"):
        badges.add("Evidence Analyst")
    PROGRESSION["completed_case_ids"].add(session["case_id"])
    PROGRESSION["best_scores"][session["case_id"]] = max(score, PROGRESSION["best_scores"].get(session["case_id"], 0))
    session["score"] = score
    return {"status": "COMPLETE", "score": score, "badges": sorted(badges), "score_events": session["score_events"], "verdict": "Evidence reconciles the anomaly; the primary signal is supported."}


@app.post("/api/sessions/{session_id}/next")
def session_next(session_id: str, request: SessionNextRequest) -> dict:
    """Serialize one logical Experiment action per process."""
    with SESSION_MUTATION_LOCK:
        return _session_next_impl(session_id, request)


def _session_next_impl(session_id: str, request: SessionNextRequest) -> dict:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Investigation not found")
    if session.get("status") == "COMPLETE":
        raise HTTPException(status_code=409, detail="Investigation is complete")
    # Client completion lists are advisory only. The server's session ledger is
    # authoritative, which prevents double-clicks or forged state from
    # repeating/skipping an Experiment.
    completed = list(session.get("completed", []))
    if session["state"] not in {HYPOTHESES_READY_STATE, EXPERIMENT_RESULT_STATE, EVIDENCE_EXPLORATION_STATE}:
        raise HTTPException(status_code=409, detail="Investigation is not ready for an experiment")
    previous = session["state"]
    session["state"] = SELECTING_EXPERIMENT_STATE
    append_event(session, "STATE", from_state=previous, to_state=session["state"])
    session["state"] = RUNNING_EXPERIMENT_STATE
    append_event(session, "STATE", from_state=SELECTING_EXPERIMENT_STATE, to_state=session["state"])
    pending = session.get("pending_decision")
    if pending and not pending.get("consumed"):
        registered = EXPERIMENTS_BY_CASE.get(session["case_id"]) or PLANNED_EXPERIMENTS_BY_CASE.get(session["case_id"], ())
        current_allowed = {item.id for item in registered if item.id not in completed}
        if pending.get("allowed_set_digest") != allowed_set_digest(current_allowed):
            session["state"] = "ERROR"
            append_event(session, "PENDING_DECISION_REJECTED", reason="STALE_ALLOWED_SET")
            raise HTTPException(status_code=409, detail="Pending Genie decision is stale")
        selected = pending["experiment_id"]
        if selected not in current_allowed:
            session["state"] = "ERROR"
            append_event(session, "PENDING_DECISION_REJECTED", reason="ALREADY_COMPLETED")
            raise HTTPException(status_code=409, detail="Pending Genie decision is no longer executable")
        index = next(i for i, item in enumerate(registered) if item.id == selected)
        result = experiment_payload(registered[index], index, session["case_id"])
        pending["consumed"] = True
        append_event(session, "PENDING_EXPERIMENT_CONSUMED", experiment_id=selected)
    else:
        try:
            result = next_experiment(ExperimentRequest(case_id=session["case_id"], completed_experiments=completed, player_prediction=request.player_prediction, conversation_id=session.get("conversation_id")))
        except HTTPException as exc:
            # Genie is advisory at this boundary.  If its control payload is
            # malformed or unavailable, continue only with the next
            # server-registered Experiment; never accept a model-provided ID.
            if exc.status_code != 503:
                session["state"] = previous
                raise
            registered = EXPERIMENTS_BY_CASE.get(session["case_id"]) or PLANNED_EXPERIMENTS_BY_CASE.get(session["case_id"], ())
            index = next((i for i, experiment in enumerate(registered) if experiment.id not in completed), None)
            if index is None:
                session["state"] = previous
                raise HTTPException(status_code=409, detail="All registered experiments are complete") from exc
            result = experiment_payload(registered[index], index, session["case_id"]) | {
                "source": "genie-server-continuation",
                "selection_note": "The server continued the next registered Experiment after an invalid Genie response.",
            }
            append_event(session, "SAFE_FALLBACK", reason="LIVE_GENIE_UNAVAILABLE_OR_INVALID")
    session["completed"] = list(dict.fromkeys(completed + [result["experiment_id"]]))
    entitlement_by_experiment = {
        "COMPONENT_DECOMPOSITION": "COMPONENT_IMPACT",
        "SNAPSHOT_DIFF": "SNAPSHOT_IMPACT",
        "DQ_MATERIALITY": "DQ_MATERIALITY",
        "FORMULA_VALIDATION": "FORMULA_VERSION",
        "RECONCILIATION": "RECONCILIATION",
    }
    tag = entitlement_by_experiment.get(result["experiment_id"])
    if tag and tag not in session.setdefault("evidence_entitlements", []):
        session["evidence_entitlements"].append(tag)
    session["score"] = session.get("score", 0)
    previous = session["state"]
    session["state"] = EXPERIMENT_RESULT_STATE
    append_event(session, "STATE", from_state=previous, to_state=session["state"])
    append_event(session, "EXPERIMENT", experiment_id=result["experiment_id"], completed=True, source=result.get("source", "fixture"))
    if genie.enabled and result.get("source") == "fixture":
        append_event(session, "SAFE_FALLBACK", reason="LIVE_GENIE_UNAVAILABLE_OR_INVALID")
    return result


@app.post("/api/experiments/next")
def next_experiment(request: ExperimentRequest) -> dict:
    try:
        case = get_any_case(request.case_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    review_mode = review_mode_enabled()
    if case_availability(case, review_mode=review_mode, completed_case_ids=PROGRESSION["completed_case_ids"]) != "AVAILABLE":
        raise HTTPException(status_code=409, detail="This Case is not enabled yet")
    experiments = EXPERIMENTS_BY_CASE.get(request.case_id) or PLANNED_EXPERIMENTS_BY_CASE.get(request.case_id, ())
    completed = set(request.completed_experiments)
    if genie.enabled and request.conversation_id:
        try:
            live = genie.next(request.conversation_id, f"Completed experiments: {sorted(completed)}; player prediction: {request.player_prediction or 'none'}", request.case_id)
            message = live["message"]
            message.update({"case_id": request.case_id, "experiment_number": len(completed) + 1, "source": "genie"})
            return message
        except Exception as exc:
            LOGGER.exception("live Genie next failed")
            # Once the server's allowed set is a singleton, no open-ended
            # model reselection is necessary. Continue with that one
            # server-owned registered Experiment and its trusted payload;
            # never accept the invalid model-selected ID.
            remaining = [experiment for experiment in experiments if experiment.id not in completed]
            if len(remaining) == 1:
                index = next(i for i, experiment in enumerate(experiments) if experiment.id == remaining[0].id)
                return experiment_payload(remaining[0], index, request.case_id) | {
                    "source": "genie-singleton-continuation",
                    "selection_note": "The server continued the only remaining allowed Experiment after an invalid Genie reselection.",
                }
            raise HTTPException(status_code=503, detail="Live Genie is unavailable") from exc
    index = next((i for i, experiment in enumerate(experiments) if experiment.id not in completed), None)
    if index is None:
        raise HTTPException(status_code=409, detail="All registered experiments are complete")
    return experiment_payload(experiments[index], index, request.case_id)


@app.post("/api/genie/ask")
def ask_genie(request: GenieQuestionRequest) -> dict:
    try:
        case = get_any_case(request.case_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if case.state != "CORE" and not review_mode_enabled():
        raise HTTPException(status_code=409, detail="This Case is not enabled yet")
    if not genie.enabled or not request.conversation_id:
        return {"answer": "Dr. Genie’s console is available when the live Genie conversation is connected.", "source": "fixture"}
    try:
        return {"answer": genie.ask(request.conversation_id, request.question), "source": "genie"}
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Genie could not answer this question") from exc


@app.post("/api/sessions/{session_id}/chat")
def session_chat(session_id: str, request: dict) -> dict:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Investigation not found")
    question = str(request.get("question", ""))
    if not question or len(question) > 1000:
        raise HTTPException(status_code=422, detail="question must be 1-1000 characters")
    now = time.monotonic()
    recent_chat = [stamp for stamp in session.setdefault("chat_timestamps", []) if now - stamp < 60]
    if len(recent_chat) >= 10:
        session["chat_timestamps"] = recent_chat
        raise HTTPException(status_code=429, detail="chat rate limit exceeded")
    recent_chat.append(now)
    session["chat_timestamps"] = recent_chat
    # Separate chat prompt boundary: prose is never passed to the control
    # parser and cannot mutate Investigation state.
    scoped_question = (
        f"You are answering a question inside MAD DATA LAB. The active Case is {session['case_id']}. "
        "Use only curated evidence for this Case. Do not reveal hidden truth or claim access to it. "
        "If evidence is insufficient, say so.\n\nUser question:\n" + question
    )
    return ask_genie(GenieQuestionRequest(case_id=session["case_id"], conversation_id=session.get("conversation_id"), question=scoped_question))


DIST = Path(__file__).resolve().parent.parent / "dist"
AXE = Path(__file__).resolve().parent.parent / "node_modules" / "axe-core"
if load_settings().local_a11y_test and AXE.exists():
    @app.get("/__test__/a11y", response_class=HTMLResponse)
    def local_a11y_harness() -> str:
        bundle = next((DIST / "assets").glob("index-*.js"), None)
        if bundle is None:
            raise HTTPException(status_code=503, detail="frontend bundle is missing")
        return f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"><title>MAD DATA LAB accessibility harness</title><script src="/__test__/axe.min.js"></script></head><body><div id="root"></div><div id="axe-result" role="status">running</div><script type="module" src="/assets/{bundle.name}"></script><script>setTimeout(()=>axe.run().then(r=>document.getElementById("axe-result").textContent=JSON.stringify({{violations:r.violations.map(v=>({{id:v.id,impact:v.impact,nodes:v.nodes.length}})),passes:r.passes.length}})),1500);</script></body></html>'''
    app.mount("/__test__", StaticFiles(directory=AXE), name="local-a11y-test")
if DIST.exists():
    app.mount("/", StaticFiles(directory=DIST, html=True), name="frontend")
