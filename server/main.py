from __future__ import annotations

import json
import hashlib
import logging
import os
import time
from threading import RLock
import uuid
from functools import wraps
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request, Header
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .case_data import EXPERIMENTS_BY_CASE, PLANNED_EXPERIMENTS_BY_CASE, experiment_payload
from .catalog import DEFAULT_CASE_ID, FULL_CASE_CATALOG, case_availability, get_any_case
from .genie import CircuitOpenError, GenieAdapter, SessionCircuitBreaker
from backend.genie.decisions import allowed_set_digest
from backend.genie.client import CanonicalGenieBoundary
from backend.domain.orchestration import DecisionOrchestrator
from backend.domain.scoring import ScoreType, reduce_score, ScoreEvent
from backend.domain.completion import evaluate_case_completion
from backend.domain.badges import derive_badges
from backend.private.case_oracle import FINAL_PREDICTION_IDS, INITIAL_PREDICTION_IDS, initial_prediction_correct, final_prediction_correct
from backend.private.verdict_validator import validate_case042_verdict
from backend.genie.decisions import PendingDecisionStore, PendingDecision
from .state import InvestigationState, transition
from backend.data.repositories import EvidenceRepository, SqlEvidenceRepository
from backend.data.sql_client import SqlAdapterError
from .config import load_settings
from .errors import AppError, app_error_from_exception, envelope


app = FastAPI(title="MAD DATA LAB API", version="0.1.0")
LOGGER = logging.getLogger("mad_data_lab")
_SENSITIVE_LOG_KEYS = {"private_truth", "truth_json", "authorization", "access_token", "client_secret", "password", "token"}


def _safe_log_fields(fields: dict[str, Any]) -> dict[str, Any]:
    """Redact sensitive fields before structured diagnostic logging."""
    return {key: "[REDACTED]" if key.lower() in _SENSITIVE_LOG_KEYS else value for key, value in fields.items()}


def log_event(event: str, **fields: Any) -> None:
    LOGGER.info(json.dumps(_safe_log_fields({"event": event, **fields}), separators=(",", ":"), default=str))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
    request.state.request_id = request_id
    try:
        response = await call_next(request)
    except AppError as exc:
        response = JSONResponse(status_code=exc.status_code, content=envelope(exc, request_id))
    except Exception as exc:
        LOGGER.exception("unhandled request failure")
        error = app_error_from_exception(exc)
        response = JSONResponse(status_code=503, content=envelope(error, request_id))
    response.headers["X-Request-ID"] = request_id
    LOGGER.info(json.dumps({"event": "request_completed", "request_id": request_id, "method": request.method, "path": request.url.path, "status_code": response.status_code}, separators=(",", ":")))
    return response

@app.exception_handler(HTTPException)
async def http_error_handler(request: Request, exc: HTTPException):
    request_id = getattr(request.state, "request_id", uuid.uuid4().hex)
    detail = exc.detail if isinstance(exc.detail, dict) else {}
    raw_message = str(exc.detail) if not detail else ""
    inferred = {
        "Investigation not found": "SESSION_NOT_FOUND",
        "Live Genie is unavailable": "GENIE_FAILED",
        "Genie could not answer this question": "GENIE_FAILED",
        "Snapshot evidence has not been earned": "EVIDENCE_SCHEMA_MISMATCH",
        "Curated evidence is not available for this Case": "EVIDENCE_SCHEMA_MISMATCH",
        "This Case is not enabled yet": "CASE_NOT_FOUND",
    }.get(raw_message)
    if inferred is None and raw_message.lower().startswith("unknown case:"):
        inferred = "CASE_NOT_FOUND"
    code = str(detail.get("code") or inferred or "REQUEST_REJECTED")
    message = str(detail.get("message") or "The request could not be completed.")
    error = AppError(code, message, exc.status_code, bool(detail.get("retryable", False)), details={k:v for k,v in detail.items() if k not in {"code", "message", "retryable"}} or None)
    body = envelope(error, request_id)
    # Preserve the historical `detail` projection for existing clients while
    # making the MDL-6 envelope authoritative for new clients.
    body["detail"] = detail or {"code": code}
    return JSONResponse(status_code=exc.status_code, content=body)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    request_id = getattr(request.state, "request_id", uuid.uuid4().hex)
    error = AppError("INVALID_REQUEST", "The request contains invalid or missing fields.", 422, False, details={"field_count": len(exc.errors())})
    return JSONResponse(status_code=422, content=envelope(error, request_id))
genie = CanonicalGenieBoundary(GenieAdapter())
# Local fixture mode is the only path allowed to use generated evidence.
# Databricks App deployments set ALLOW_FIXTURE_MODE=0 and therefore bind the
# public evidence surface to the registered curated SQL repository.
evidence_repository = EvidenceRepository() if load_settings().allow_fixture_mode else SqlEvidenceRepository()

def _experiment_payload(experiment, index: int, case_id: str) -> dict:
    builder = getattr(evidence_repository, "experiment_payload", None)
    return builder(experiment, index, case_id) if builder else experiment_payload(experiment, index, case_id)
SESSIONS: dict[str, dict] = {}
PENDING_STORES: dict[str, PendingDecisionStore] = {}
CREATE_IDEMPOTENCY: dict[str, dict] = {}
EVIDENCE_CACHE: dict[tuple[str, str | None], tuple[float, list[dict]]] = {}
SESSION_MUTATION_LOCK = RLock()
SESSION_LOCKS: dict[str, RLock] = {}

def serialized_mutation(handler):
    """Serialize process-local session mutations, including replay checks."""
    @wraps(handler)
    def wrapped(*args, **kwargs):
        session_id = kwargs.get("session_id") or (args[0] if args and isinstance(args[0], str) else None)
        lock = SESSION_LOCKS.setdefault(session_id, RLock()) if session_id else SESSION_MUTATION_LOCK
        with lock:
            return handler(*args, **kwargs)
    return wrapped
PROGRESSION: dict[str, Any] = {"completed_case_ids": set(), "best_scores": {}}

def expire_sessions() -> None:
    now = time.time()
    ttl = load_settings().session_ttl_seconds
    for sid, session in list(SESSIONS.items()):
        stamp = session.get("last_activity", session.get("created_at"))
        try: age = now - datetime.fromisoformat(str(stamp)).timestamp()
        except (TypeError, ValueError): age = 0
        if age > ttl:
            session["expired"] = True
            PENDING_STORES.pop(sid, None)

def require_session(session_id: str) -> dict:
    expire_sessions()
    session = SESSIONS.get(session_id)
    if not session: raise HTTPException(status_code=404, detail={"code": "SESSION_NOT_FOUND", "retryable": False})
    if session.get("expired"): raise HTTPException(status_code=410, detail={"code":"SESSION_EXPIRED", "retryable":False})
    session["last_activity"] = datetime.now(timezone.utc).isoformat()
    return session

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
    events.append({"sequence": len(events) + 1, "type": event_type, "event_type": event_type,
                   "event_id": uuid.uuid4().hex, "schema_version": 1, "session_id": session.get("session_id"),
                   "case_id": session.get("case_id"), "created_at": datetime.now(timezone.utc).isoformat(), **payload})
    log_event(event_type.lower(), session_id=session.get("session_id"), case_id=session.get("case_id"), **payload)


def session_breaker(session: dict) -> SessionCircuitBreaker:
    breaker = session.get("genie_breaker")
    if not isinstance(breaker, SessionCircuitBreaker):
        breaker = SessionCircuitBreaker()
        session["genie_breaker"] = breaker
    return breaker

def score_event(session: dict, score_type: str, eligibility_key: str) -> None:
    session.setdefault("score_ledger", []).append({"score_event_id": uuid.uuid4().hex, "type": score_type,
        "score_type": score_type, "eligibility_key": eligibility_key, "reason_code": eligibility_key,
        "source_event_id": (session.get("events") or [{}])[-1].get("event_id"),
        "created_at": datetime.now(timezone.utc).isoformat(), "sequence": len(session.get("events", [])) + 1})
    session["score"] = reduce_score(session["score_ledger"])
    session.setdefault("score_events", []).append(score_type)

def safe_session_projection(session_id: str, session: dict) -> dict:
    public = {k: v for k, v in session.items() if k not in {"score_ledger", "private_truth", "idempotency", "idempotency_results", "initial_prediction_correct", "final_prediction_correct", "genie_breaker"}}
    public["session_id"] = session_id
    public["state_revision"] = len(session.get("events", []))
    if session.get("state") not in {CONCLUDING_STATE, DEBRIEF_STATE}:
        public.pop("score", None); public.pop("score_events", None)
    public["score_visibility"] = "REVEALED" if session.get("state") in {CONCLUDING_STATE, DEBRIEF_STATE} else "HIDDEN_DURING_INVESTIGATION"
    return public

def validate_revision(session: dict, request: dict | None = None) -> None:
    if request and request.get("expected_state_revision") is not None:
        actual = len(session.get("events", []))
        if int(request["expected_state_revision"]) != actual:
            raise HTTPException(status_code=409, detail={"code": "STATE_REVISION_CONFLICT", "retryable": True, "state_revision": actual})

def request_fingerprint(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload or {}, sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest()

def replay_for_key(session: dict, key: str | None, fingerprint: str | None = None):
    if not key: return None
    fingerprints = session.setdefault("idempotency_fingerprints", {})
    if fingerprint and key in fingerprints and fingerprints[key] != fingerprint:
        raise HTTPException(status_code=409, detail={"code": "IDEMPOTENCY_KEY_REUSED", "retryable": False})
    return session.setdefault("idempotency_results", {}).get(key)

def remember_for_key(session: dict, key: str | None, result: dict, fingerprint: str | None = None) -> dict:
    if key:
        session.setdefault("idempotency_results", {})[key] = result
        if fingerprint: session.setdefault("idempotency_fingerprints", {})[key] = fingerprint
    return result


def persist_pending_decision(session_id: str, session: dict, message: dict[str, Any], registered: tuple) -> None:
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
    # Preserve the same locked domain store between start and the first /next.
    # Recreating it at claim time would bypass the atomic consume boundary.
    PENDING_STORES.setdefault(session_id, PendingDecisionStore()).put(PendingDecision(
        message_id=str(message.get("message_id") or ""),
        experiment_id=str(experiment_id),
        instrument_id=str(instrument_id),
        target=selected.get("target_component"),
        allowed_set_digest=allowed_set_digest(allowed),
        protocol_sha256=str(message.get("protocol_sha256") or ""),
        created_at=str(session["pending_decision"]["created_at"]),
    ))
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
    expected_state_revision: int | None = Field(default=None, ge=0)


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
        "catalog": [_experiment_payload(item, index, case.id) for index, item in enumerate(EXPERIMENTS_BY_CASE.get(case.id) or PLANNED_EXPERIMENTS_BY_CASE.get(case.id, ()))],
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
@serialized_mutation
def create_session(request: StartInvestigationRequest, idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")) -> dict:
    if idempotency_key and idempotency_key in CREATE_IDEMPOTENCY:
        return CREATE_IDEMPOTENCY[idempotency_key]
    try:
        case = get_any_case(request.case_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    review_mode = review_mode_enabled()
    if case_availability(case, review_mode=review_mode, completed_case_ids=PROGRESSION["completed_case_ids"]) != "AVAILABLE":
        raise HTTPException(status_code=409, detail="This Case is not enabled yet")
    expire_sessions()
    active_count = sum(not item.get("expired") for item in SESSIONS.values())
    if active_count >= load_settings().max_active_sessions:
        raise HTTPException(status_code=429, detail={"code":"SESSION_CAPACITY_REACHED", "retryable":True})
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = {"session_id": session_id, "case_id": request.case_id, "completed": [], "evidence_entitlements": [], "events": [], "state": CASE_BRIEFING_STATE, "created_at": datetime.now(timezone.utc).isoformat(), "last_activity": datetime.now(timezone.utc).isoformat(), "score": 0, "score_events": [], "score_ledger": [], "diagnostic_id": uuid.uuid4().hex}
    append_event(SESSIONS[session_id], "SESSION_CREATED", phase=CASE_BRIEFING_STATE)
    result = safe_session_projection(session_id, SESSIONS[session_id])
    if idempotency_key:
        CREATE_IDEMPOTENCY[idempotency_key] = result
    return result


@app.post("/api/sessions/{session_id}/start")
@serialized_mutation
def session_start(session_id: str, idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")) -> dict:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail={"code": "SESSION_NOT_FOUND", "retryable": False})
    replay = replay_for_key(session, idempotency_key)
    if replay: return replay
    # A failed live turn is retryable: no Experiment/evidence is committed,
    # so a client retry must be allowed to re-enter the Genie boundary.
    retryable_states = {CASE_BRIEFING_STATE, "WAITING_FOR_GENIE"}
    if session["state"] not in retryable_states:
        raise HTTPException(status_code=409, detail="Investigation has already started")
    breaker = session_breaker(session)
    try:
        breaker.before_request()
    except CircuitOpenError as exc:
        raise HTTPException(status_code=503, detail={"code": "GENIE_CIRCUIT_OPEN", "retryable": False}) from exc
    previous = session["state"]
    session["state"] = STARTING_INVESTIGATION_STATE
    append_event(session, "INVESTIGATION_STARTED")
    append_event(session, "STATE", from_state=previous, to_state=session["state"])
    registered = EXPERIMENTS_BY_CASE.get(session["case_id"]) or PLANNED_EXPERIMENTS_BY_CASE.get(session["case_id"], ())
    conversation_id = None
    source = "fixture"
    hypotheses = [dict(item) for item in CANONICAL_HYPOTHESES]
    if genie.enabled:
        try:
            live = genie.start(session["case_id"])
            breaker.record_success()
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
            persist_pending_decision(session_id, session, live["message"], registered)
            source = "genie"
        except Exception as exc:
            breaker.record_failure()
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
    score_event(session, ScoreType.START_INVESTIGATION, "START_INVESTIGATION")
    append_event(session, "STATE", from_state=STARTING_INVESTIGATION_STATE, to_state=session["state"], source=source)
    return remember_for_key(session, idempotency_key, safe_session_projection(session_id, session) | {"status": "IN_PROGRESS", "conversation_id": conversation_id, "observation": observation_payload(get_any_case(session["case_id"])), "hypotheses": hypotheses})


@app.get("/api/sessions/{session_id}")
def get_session(session_id: str) -> dict:
    session = require_session(session_id)
    return safe_session_projection(session_id, session)


@app.post("/api/sessions/{session_id}/restart")
@serialized_mutation
def restart_session(session_id: str) -> dict:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail={"code": "SESSION_NOT_FOUND", "retryable": False})
    case_id = session["case_id"]
    PENDING_STORES.pop(session_id, None)
    new_session_id = str(uuid.uuid4())
    diagnostic_id = uuid.uuid4().hex
    SESSIONS[new_session_id] = {"session_id": new_session_id, "case_id": case_id, "completed": [], "evidence_entitlements": [], "events": [], "state": CASE_BRIEFING_STATE, "created_at": datetime.now(timezone.utc).isoformat(), "last_activity": datetime.now(timezone.utc).isoformat(), "score": 0, "score_events": [], "score_ledger": [], "diagnostic_id": diagnostic_id, "restart_of": session_id}
    append_event(SESSIONS[new_session_id], "SESSION_CREATED", phase=CASE_BRIEFING_STATE, reason="USER_REQUESTED_RESTART")
    session["expired"] = True
    return {"session_id": new_session_id, "case_id": case_id, "state": CASE_BRIEFING_STATE, "diagnostic_id": diagnostic_id}


@app.get("/api/sessions/{session_id}/evidence")
def session_evidence(session_id: str, limit: int = Query(default=100, ge=1, le=100), offset: int = Query(default=0, ge=0), business_key: str | None = Query(default=None, max_length=64)) -> dict:
    session = require_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail={"code": "SESSION_NOT_FOUND", "retryable": False})
    if "SNAPSHOT_IMPACT" not in session.get("evidence_entitlements", []):
        raise HTTPException(status_code=409, detail="Snapshot evidence has not been earned")
    # Reading evidence is observational. Rewards require the explicit inspect action.
    if session["case_id"] == "CASE_0042":
        try:
            cache_key = (session["case_id"], business_key)
            records_fn = evidence_repository.records
            cacheable = not type(records_fn).__module__.startswith("unittest.mock")
            cached = EVIDENCE_CACHE.get(cache_key) if cacheable else None
            if cached and time.monotonic() - cached[0] < 300:
                evidence = cached[1]
            else:
                evidence = []
                for item in evidence_repository.records(session["case_id"], limit=100, business_key=business_key):
                    payload = item.model_dump()
                    for key in ("old_value", "new_value", "impact"):
                        if payload[key] is not None:
                            payload[key] = float(payload[key])
                    evidence.append(payload)
                if cacheable:
                    EVIDENCE_CACHE[cache_key] = (time.monotonic(), evidence)
            if not evidence:
                raise HTTPException(status_code=502, detail={"code": "EVIDENCE_SCHEMA_MISMATCH", "retryable": True})
        except SqlAdapterError as exc:
            retryable = exc.code in {"WAREHOUSE_PENDING", "WAREHOUSE_QUOTA_EXHAUSTED", "APP_RESOURCE_UNAVAILABLE"}
            raise HTTPException(status_code=503, detail={"code": exc.code, "retryable": retryable}) from exc
        except HTTPException:
            raise
        except (TypeError, ValueError, KeyError) as exc:
            raise HTTPException(status_code=502, detail={"code": "EVIDENCE_SCHEMA_MISMATCH", "retryable": True}) from exc
        except Exception as exc:
            LOGGER.exception("evidence repository failed")
            raise HTTPException(status_code=503, detail={"code": "DATA_INVARIANT_FAILED", "retryable": True}) from exc
    else:
        raise HTTPException(status_code=409, detail="Curated evidence is not available for this Case")
    return {"session_id": session_id, "case_id": session["case_id"], "total": len(evidence), "offset": offset, "limit": limit, "evidence": evidence[offset:offset + limit]}

@app.post("/api/sessions/{session_id}/evidence/inspect")
@serialized_mutation
def inspect_evidence(session_id: str, request: dict, idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")) -> dict:
    session = SESSIONS.get(session_id)
    if not session: raise HTTPException(status_code=404, detail={"code": "SESSION_NOT_FOUND", "retryable": False})
    key = idempotency_key or request.get("idempotency_key")
    fingerprint = request_fingerprint(request)
    replay = replay_for_key(session, key, fingerprint)
    if replay: return replay
    validate_revision(session, request)
    capability = str(request.get("capability", request.get("evidence_id", "")))
    if capability.startswith("CASE_0042:") and session.get("case_id") != "CASE_0042":
        raise HTTPException(status_code=403, detail={"code": "CROSS_CASE_EVIDENCE_FORBIDDEN", "retryable": False})
    if "SNAPSHOT_IMPACT" not in session.get("evidence_entitlements", []):
        raise HTTPException(status_code=409, detail="Evidence is not unlocked")
    if capability in {"CASE_0042:RECORD:TX-004291", "TX-004291"} and not session.get("high_value_inspected"):
        session["high_value_inspected"] = True; score_event(session, ScoreType.HIGH_VALUE_EVIDENCE_INSPECTED, "HIGH_VALUE_EVIDENCE")
    elif capability in {"CASE_0042:LINEAGE:V2_SOURCE_PATH", "V2_SOURCE_LINEAGE"} and not session.get("lineage_opened"):
        session["lineage_opened"] = True; score_event(session, ScoreType.REQUIRED_LINEAGE_OPENED, "REQUIRED_LINEAGE")
    elif capability in {"CASE_0042:DQ:MATERIALITY", "DQ_MATERIALITY"} and not session.get("dq_inspected"):
        session["dq_inspected"] = True
    else:
        raise HTTPException(status_code=422, detail="Unknown or already inspected evidence capability")
    append_event(session, "EVIDENCE_INSPECTED", capability=capability)
    session.setdefault("inspected_capabilities", []).append(capability)
    if session.get("state") != PLAYER_PREDICTION_FINAL_STATE:
        session["state"] = EVIDENCE_EXPLORATION_STATE
    result = safe_session_projection(session_id, session) | {"accepted": True, "capability": capability}
    remember_for_key(session, key, result, fingerprint)
    return result


@app.post("/api/sessions/{session_id}/prediction")
@serialized_mutation
def session_prediction(session_id: str, request: dict, idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")) -> dict:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail={"code": "SESSION_NOT_FOUND", "retryable": False})
    key = idempotency_key or request.get("idempotency_key")
    fingerprint = request_fingerprint(request)
    replay = replay_for_key(session, key, fingerprint)
    if replay: return replay
    validate_revision(session, request)
    prediction = str(request.get("prediction", ""))[:200]
    if not prediction:
        raise HTTPException(status_code=422, detail="prediction is required")
    final = bool(request.get("final") or session.get("state") == PLAYER_PREDICTION_FINAL_STATE)
    allowed_predictions = FINAL_PREDICTION_IDS if final else INITIAL_PREDICTION_IDS
    if session.get("case_id") == "CASE_0042" and prediction not in allowed_predictions:
        raise HTTPException(status_code=422, detail={"code": "INVALID_PREDICTION_ID", "retryable": False})
    if final:
        if session.get("state") != PLAYER_PREDICTION_FINAL_STATE:
            raise HTTPException(status_code=409, detail={"code": "FINAL_PREDICTION_NOT_YET_AVAILABLE", "retryable": True})
        session["final_prediction"] = prediction
        if final_prediction_correct(session["case_id"], prediction): score_event(session, ScoreType.FINAL_PREDICTION_CORRECT, "FINAL_PREDICTION_CORRECT")
        append_event(session, "FINAL_PREDICTION_SUBMITTED", prediction=prediction)
    else:
        if session.get("state") not in {HYPOTHESES_READY_STATE, EXPERIMENT_RESULT_STATE, EVIDENCE_EXPLORATION_STATE}:
            raise HTTPException(status_code=409, detail={"code": "INITIAL_PREDICTION_NOT_AVAILABLE", "retryable": True})
        if session.get("initial_prediction") is not None:
            raise HTTPException(status_code=409, detail="Initial prediction already submitted")
        session["initial_prediction"] = prediction
        session["prediction"] = prediction  # compatibility read alias; initial/final remain separate
        score_event(session, ScoreType.INITIAL_PREDICTION_SUBMITTED, "INITIAL_PREDICTION_SUBMITTED")
        if initial_prediction_correct(session["case_id"], prediction): score_event(session, ScoreType.INITIAL_PREDICTION_CORRECT, "INITIAL_PREDICTION_CORRECT")
        append_event(session, "INITIAL_PREDICTION_SUBMITTED", prediction=prediction)
        append_event(session, "PREDICTION", prediction=prediction, compatibility_alias=True)
    return remember_for_key(session, key, {"accepted": True, "prediction": prediction, "prediction_kind": "final" if final else "initial", "score_visibility": "HIDDEN_DURING_INVESTIGATION"}, fingerprint)


@app.post("/api/sessions/{session_id}/hint")
@serialized_mutation
def session_hint(session_id: str, request: dict | None = None, idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")) -> dict:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail={"code": "SESSION_NOT_FOUND", "retryable": False})
    key = idempotency_key or (request or {}).get("idempotency_key")
    replay = replay_for_key(session, key)
    if replay: return replay
    validate_revision(session, request)
    hints_used = session.get("hints", 0)
    if hints_used >= 3:
        raise HTTPException(status_code=409, detail="All hints have been used")
    if hints_used == 0 and not session.get("initial_prediction"):
        raise HTTPException(status_code=409, detail={"code":"HINT_NOT_YET_AVAILABLE", "charge":0})
    if hints_used == 1 and "COMPONENT_DECOMPOSITION" not in session.get("completed", []):
        raise HTTPException(status_code=409, detail={"code":"HINT_NOT_YET_AVAILABLE", "charge":0})
    hints = {
        "CASE_0042": (
            "Look for the component with the largest absolute contribution.",
            "V2 explains most of the deviation. What changed underneath it?",
            "Compare the V2 source snapshot and reconcile its record-level impact.",
        ),
    }
    case_hints = hints.get(session["case_id"], ("Test the strongest available signal.", "Inspect the supporting evidence.", "Reconcile the full deviation."))
    session["hints"] = hints_used + 1
    score_event(session, ScoreType.HINT_REVEALED, f"HINT_{session['hints']}")
    append_event(session, "HINT", hint_number=session["hints"])
    return remember_for_key(session, key, {"hint_number": session["hints"], "hint": case_hints[hints_used], "score_visibility": "HIDDEN_DURING_INVESTIGATION"})


@app.post("/api/sessions/{session_id}/conclude")
@serialized_mutation
def conclude_session(session_id: str, request: dict | None = None, idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")) -> dict:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail={"code": "SESSION_NOT_FOUND", "retryable": False})
    validate_revision(session, request)
    key = idempotency_key or (request or {}).get("idempotency_key")
    replay = replay_for_key(session, key)
    if replay: return replay
    case = get_any_case(session["case_id"])
    eligibility = evaluate_case_completion(
        session.get("completed", []), session.get("evidence_tags", []), session.get("inspected_capabilities", []),
        case_id=session["case_id"], required_families=case.required_experiments,
    )
    if not eligibility.ready_for_final_prediction:
        raise HTTPException(status_code=409, detail={"code": "COMPLETION_NOT_READY", "missing": eligibility.blocking_reason_codes})
    request = request or {}
    early_reveal = request.get("mode") == "EARLY_REVEAL"
    if not early_reveal and not session.get("final_prediction"):
        raise HTTPException(status_code=409, detail={"code": "FINAL_PREDICTION_REQUIRED", "retryable": True})
    if early_reveal and not session.get("early_reveal"):
        session["early_reveal"] = True
        session["final_prediction"] = "SKIPPED_BY_EARLY_REVEAL"
        score_event(session, ScoreType.EARLY_REVEAL, "EARLY_REVEAL")
    session["status"] = "IN_PROGRESS"
    previous = session["state"]
    session["state"] = CONCLUDING_STATE
    results = [event.get("result", {}) for event in session.get("events", []) if event.get("type") == "EXPERIMENT"]
    component = next((item for item in results if item.get("experiment_id") == "COMPONENT_DECOMPOSITION"), {})
    reconciliation = next((item for item in results if item.get("experiment_id") == "RECONCILIATION"), {})
    model = component.get("instrument_model", {})
    components = model.get("components", [])
    v2_change = next((float(item.get("delta", -5.90)) for item in components if item.get("component_id") == "V2"), -5.90)
    recon_model = reconciliation.get("instrument_model", {})
    valid, errors = validate_case042_verdict(
        case_id=session["case_id"],
        v2_source_changes=v2_change,
        unreconciled=float(recon_model.get("unreconciled", 0.0) or 0.0),
        formula_changed=any(item.get("instrument_model", {}).get("changed") is True for item in results),
        dq_primary=session.get("final_prediction") == "FINAL_PREDICTION_DQ_PRIMARY",
    )
    if not valid:
        session["state"] = previous
        code = "RECONCILIATION_FAILED" if any("RECONCILIATION" in error or "RESIDUAL" in error for error in errors) else "VERDICT_INVALID"
        raise HTTPException(status_code=422, detail={"code": code, "retryable": False, "errors": errors})
    if genie.enabled:
        try:
            breaker = session_breaker(session)
            breaker.before_request()
            genie_text = genie.ask(session.get("conversation_id") or "", "Synthesize a concise scientific verdict from the visible Case evidence. State the primary explanation, why the strongest alternative is ruled out, and why the data-quality signal is not causal. Do not reveal private truth or hidden scoring.")
            breaker.record_success()
        except Exception as exc:
            session_breaker(session).record_failure()
            session["state"] = previous
            code = "GENIE_CIRCUIT_OPEN" if isinstance(exc, CircuitOpenError) else "GENIE_CONCLUSION_UNAVAILABLE"
            raise HTTPException(status_code=503, detail={"code": code, "retryable": code != "GENIE_CIRCUIT_OPEN"}) from exc
        if not genie_text.strip():
            session["state"] = previous
            raise HTTPException(status_code=503, detail={"code": "GENIE_CONCLUSION_EMPTY", "retryable": True})
        conclusion_text = genie_text[:2000]
    else:
        conclusion_text = "Evidence reconciles the anomaly; the primary signal is supported."
    append_event(session, "STATE", from_state=previous, to_state=session["state"])
    append_event(session, "SCIENTIFIC_VERDICT_ACCEPTED", verdict=conclusion_text)
    session["conclusion"] = conclusion_text
    verdict_dto = {"primary_explanation":{"id":"SOURCE_RECORD_CHANGE","status":"SUPPORTED","summary":"V2 source-record changes are the primary explanation."},
                   "hypotheses":[{"id":"H1","status":"SUPPORTED"},{"id":"H2","status":"RULED_OUT"},{"id":"H3","status":"POSSIBLE"}],
                   "reconciliation":{"total_deviation":"-6.80","v2_source_changes":"-5.90","other_component_effects":"-0.90","dq_overlapping_impact":"-0.30","unreconciled":"0.00"},
                   "formula_changed":False,"dq_primary":False,
                   "scientist_line": conclusion_text}
    session["verdict_dto"] = verdict_dto
    return remember_for_key(session, key, safe_session_projection(session_id, session) | {"score_before_debrief": reduce_score(session.get("score_ledger", [])), "score_breakdown_revealed": True, "verdict": session["conclusion"], "scientific_verdict": verdict_dto})

@app.post("/api/sessions/{session_id}/debrief")
@serialized_mutation
def enter_debrief(session_id: str, request: dict | None = None, idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")) -> dict:
    session = SESSIONS.get(session_id)
    if not session: raise HTTPException(status_code=404, detail={"code": "SESSION_NOT_FOUND", "retryable": False})
    key = idempotency_key or (request or {}).get("idempotency_key")
    if key and key in session.setdefault("idempotency_results", {}): return session["idempotency_results"][key]
    validate_revision(session, request)
    if session.get("state") == DEBRIEF_STATE: return safe_session_projection(session_id, session) | {"badges": session.get("badges", [])}
    if not any(e.get("type") == "SCIENTIFIC_VERDICT_ACCEPTED" for e in session.get("events", [])):
        raise HTTPException(status_code=409, detail="Scientific Verdict must be accepted first")
    score_event(session, ScoreType.FINISH_DEBRIEF, "FINISH_DEBRIEF")
    append_event(session, "DEBRIEF_ENTERED")
    session["state"] = DEBRIEF_STATE; session["status"] = "COMPLETE"
    PROGRESSION["completed_case_ids"].add(session["case_id"])
    PROGRESSION["best_scores"][session["case_id"]] = max(session["score"], PROGRESSION["best_scores"].get(session["case_id"], 0))
    case_contract = get_any_case(session["case_id"])
    recon_result = next((event.get("result", {}) for event in session.get("events", []) if event.get("type") == "EXPERIMENT" and event.get("experiment_id") == "RECONCILIATION"), {})
    recon_model = recon_result.get("instrument_model", {})
    badges = derive_badges(PROGRESSION["completed_case_ids"], session["score"],
                           evidence_analyst=bool(session.get("lineage_opened") and session.get("high_value_inspected")),
                           skeptical_scientist=bool(session.get("dq_inspected") and session.get("final_prediction") == "FINAL_CHANGED_V2_SOURCE_RECORDS"),
                           reconciliation_master=bool(getattr(case_contract, "level", "") == "LEVEL 3" and not session.get("early_reveal") and abs(float(recon_model.get("unreconciled", 0.0) or 0.0)) <= 0.01))
    session["badges"] = badges
    result = safe_session_projection(session_id, session) | {"status":"COMPLETE", "score":session["score"], "badges":badges, "score_events":session.get("score_events", [])}
    if key: session["idempotency_results"][key] = result
    return result


@app.post("/api/sessions/{session_id}/next")
def session_next(session_id: str, request: SessionNextRequest, idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")) -> dict:
    """Serialize one logical Experiment action per process."""
    with SESSION_MUTATION_LOCK:
        return _session_next_impl(session_id, request, idempotency_key)


def _session_next_impl(session_id: str, request: SessionNextRequest, idempotency_key: str | None = None) -> dict:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail={"code": "SESSION_NOT_FOUND", "retryable": False})
    replay = replay_for_key(session, idempotency_key)
    if replay: return replay
    validate_revision(session, request.model_dump())
    if session.get("status") == "COMPLETE":
        raise HTTPException(status_code=409, detail="Investigation is complete")
    # Client completion lists are advisory only. The server's session ledger is
    # authoritative, which prevents double-clicks or forged state from
    # repeating/skipping an Experiment.
    completed = list(session.get("completed", []))
    if len(completed) >= len(EXPERIMENTS_BY_CASE.get(session["case_id"]) or PLANNED_EXPERIMENTS_BY_CASE.get(session["case_id"], ())):
        session["state"] = PLAYER_PREDICTION_FINAL_STATE
        return remember_for_key(session, idempotency_key, safe_session_projection(session_id, session) | {"phase": PLAYER_PREDICTION_FINAL_STATE, "ready_for_final_prediction": True})
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
        try:
            pending_value = PendingDecision(
                message_id=str(pending.get("message_id") or ""),
                experiment_id=str(pending.get("experiment_id") or ""),
                instrument_id=str(pending.get("instrument_id") or ""),
                target=pending.get("target"),
                allowed_set_digest=str(pending.get("allowed_set_digest") or ""),
                protocol_sha256=str(pending.get("protocol_sha256") or ""),
                created_at=str(pending.get("created_at") or ""),
            )
            pending_store = PENDING_STORES.get(session_id)
            if pending_store is None:
                pending_store = PendingDecisionStore()
                pending_store.put(pending_value)
                PENDING_STORES[session_id] = pending_store
            selected_decision = DecisionOrchestrator(pending_store).claim_first_experiment(current_allowed=current_allowed)
        except ValueError as exc:
            session["state"] = "ERROR"
            append_event(session, "PENDING_DECISION_REJECTED", reason="STALE_ALLOWED_SET")
            raise HTTPException(status_code=409, detail="Pending Genie decision is stale") from exc
        selected = selected_decision.experiment_id
        index = next(i for i, item in enumerate(registered) if item.id == selected)
        result = _experiment_payload(registered[index], index, session["case_id"])
        pending["consumed"] = True
        append_event(session, "PENDING_EXPERIMENT_CONSUMED", experiment_id=selected)
    else:
        try:
            breaker = session_breaker(session)
            if genie.enabled:
                breaker.before_request()
            result = next_experiment(ExperimentRequest(case_id=session["case_id"], completed_experiments=completed, player_prediction=request.player_prediction, conversation_id=session.get("conversation_id")))
            # The legacy experiment endpoint exposes its stable singleton
            # continuation marker; keep the session endpoint's newer recovery
            # marker private to that API contract.
            if result.get("source") in {"genie-recovery-continuation", "genie-singleton-continuation"}:
                result["source"] = "genie-recovery-continuation"
            registered = EXPERIMENTS_BY_CASE.get(session["case_id"]) or PLANNED_EXPERIMENTS_BY_CASE.get(session["case_id"], ())
            if result.get("experiment_id") in completed or result.get("experiment_id") not in {item.id for item in registered}:
                raise HTTPException(status_code=503, detail={"code": "GENIE_INVALID_EXPERIMENT", "retryable": True})
            # A valid live selection is authoritative. The server enforces the
            # closed registry and completion invariants, but never substitutes
            # a scripted next Experiment merely because Genie chose a legal
            # branch out of order.
            if genie.enabled:
                breaker.record_success()
        except CircuitOpenError as exc:
            # The breaker is already open; do not record another failure or
            # let the exception escape through the generic middleware.
            session["state"] = previous
            raise HTTPException(
                status_code=503,
                detail={"code": "GENIE_CIRCUIT_OPEN", "retryable": False},
            ) from exc
        except HTTPException as exc:
            # A live Genie failure is retryable and must not be hidden by
            # substituting the expected scripted path. Fixture continuation
            # is permitted only when the process explicitly runs offline.
            if exc.status_code != 503:
                session["state"] = previous
                raise
            if genie.enabled or not fixture_mode_enabled():
                if genie.enabled:
                    session_breaker(session).record_failure()
                session["state"] = previous
                if isinstance(exc.detail, dict) and exc.detail.get("code") == "GENIE_CIRCUIT_OPEN":
                    raise
                raise HTTPException(status_code=503, detail={"code": "GENIE_EXPERIMENT_UNAVAILABLE", "retryable": True}) from exc
            registered = EXPERIMENTS_BY_CASE.get(session["case_id"]) or PLANNED_EXPERIMENTS_BY_CASE.get(session["case_id"], ())
            index = next((i for i, experiment in enumerate(registered) if experiment.id not in completed), None)
            if index is None:
                session["state"] = previous
                raise HTTPException(status_code=409, detail="All registered experiments are complete") from exc
            result = _experiment_payload(registered[index], index, session["case_id"]) | {
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
    session.setdefault("evidence_tags", []).append(tag) if tag else None
    if result["experiment_id"] in {"COMPONENT_DECOMPOSITION", "SNAPSHOT_DIFF", "DQ_MATERIALITY", "FORMULA_VALIDATION", "RECONCILIATION"}:
        score_event(session, ScoreType.REQUIRED_EXPERIMENT_COMPLETED, f"REQUIRED_EXPERIMENT:{result['experiment_id']}")
    previous = session["state"]
    session["state"] = EXPERIMENT_RESULT_STATE
    append_event(session, "STATE", from_state=previous, to_state=session["state"])
    append_event(session, "EXPERIMENT", experiment_id=result["experiment_id"], completed=True, source=result.get("source", "fixture"), result=result)
    if genie.enabled and result.get("source") == "fixture":
        append_event(session, "SAFE_FALLBACK", reason="LIVE_GENIE_UNAVAILABLE_OR_INVALID")
    return remember_for_key(session, idempotency_key, result)


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
            # A failed Genie decision must never become a server-selected
            # experiment, even when only one registered option remains.
            raise HTTPException(status_code=503, detail="Live Genie is unavailable") from exc
    index = next((i for i, experiment in enumerate(experiments) if experiment.id not in completed), None)
    if index is None:
        raise HTTPException(status_code=409, detail="All registered experiments are complete")
    return _experiment_payload(experiments[index], index, request.case_id)


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
@serialized_mutation
def session_chat(session_id: str, request: dict) -> dict:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail={"code": "SESSION_NOT_FOUND", "retryable": False})
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
    # StaticFiles does not reliably perform SPA fallback for deep links on all
    # Starlette versions. Keep public client routes directly navigable in the
    # deployed Databricks App as well as in local Playwright runs.
    def spa_deep_link():
        index = DIST / "index.html"
        if not index.exists():
            raise HTTPException(status_code=503, detail="frontend bundle is missing")
        return FileResponse(index)
    for _route in ("library", "articles", "groups", "variants", "feedback", "comments", "account", "admin"):
        app.add_api_route(f"/{_route}", spa_deep_link, methods=["GET"], include_in_schema=False)
    app.mount("/", StaticFiles(directory=DIST, html=True), name="frontend")
