from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .case_data import EXPERIMENTS_BY_CASE, PLANNED_EXPERIMENTS_BY_CASE, experiment_payload
from .catalog import FULL_CASE_CATALOG, case_availability, get_any_case
from .genie import GenieAdapter
from .domain import generate_case
from .state import InvestigationState, transition


app = FastAPI(title="MAD DATA LAB API", version="0.1.0")
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
genie = GenieAdapter()
SESSIONS: dict[str, dict] = {}
PROGRESSION: dict[str, Any] = {"completed_case_ids": set(), "best_scores": {}}


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



class StartInvestigationRequest(BaseModel):
    case_id: str = Field(default="CASE_0042", pattern=r"^CASE_\d{4}$")


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
    return {"status": "ok", "genie_mode": "live" if genie.enabled else "fixture"}


@app.get("/api/cases")
def cases() -> dict:
    review_mode = os.getenv("CHALLENGE_REVIEW_MODE", "0") == "1"
    completed = PROGRESSION["completed_case_ids"]
    return {"cases": [case.public_payload() | {"availability": case_availability(case, review_mode=review_mode, completed_case_ids=completed)} for case in FULL_CASE_CATALOG]}


@app.get("/api/health")
def api_health() -> dict[str, str]:
    return health()


@app.get("/api/config")
def config() -> dict:
    review_mode = os.getenv("CHALLENGE_REVIEW_MODE", "0") == "1"
    enabled = [c.id for c in FULL_CASE_CATALOG if case_availability(c, review_mode=review_mode, completed_case_ids=PROGRESSION["completed_case_ids"]) == "AVAILABLE"]
    return {"protocol_version": "1.0", "fixture_mode": not genie.enabled, "review_mode": review_mode, "enabled_cases": enabled}


@app.get("/api/progression")
def progression() -> dict:
    completed = sorted(PROGRESSION["completed_case_ids"])
    best_scores = dict(PROGRESSION["best_scores"])
    review_mode = os.getenv("CHALLENGE_REVIEW_MODE", "0") == "1"
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
    review_mode = os.getenv("CHALLENGE_REVIEW_MODE", "0") == "1"
    if case_availability(case, review_mode=review_mode, completed_case_ids=PROGRESSION["completed_case_ids"]) != "AVAILABLE":
        raise HTTPException(status_code=409, detail="This Case is not enabled yet")
    registered_experiments = EXPERIMENTS_BY_CASE.get(request.case_id) or PLANNED_EXPERIMENTS_BY_CASE.get(request.case_id, ())
    if genie.enabled:
        try:
            live = genie.start(request.case_id)
            session_id = str(uuid.uuid4())
            SESSIONS[session_id] = {"case_id": request.case_id, "completed": [], "events": [], "state": InvestigationState.BRIEFING.value, "created_at": datetime.now(timezone.utc).isoformat(), "score": 50, "score_events": ["START_INVESTIGATION"], "conversation_id": live["conversation_id"], "diagnostic_id": uuid.uuid4().hex}
            return {"investigation_id": session_id, "session_id": session_id, "conversation_id": live["conversation_id"], "case_id": request.case_id, "observation": observation_payload(case), "hypotheses": [name for name, _ in registered_experiments[0].updates] if registered_experiments else [], "source": "genie"}
        except Exception:
            pass
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = {"case_id": request.case_id, "completed": [], "events": [], "state": InvestigationState.BRIEFING.value, "created_at": datetime.now(timezone.utc).isoformat(), "score": 50, "score_events": ["START_INVESTIGATION"], "diagnostic_id": uuid.uuid4().hex}
    return {
        "investigation_id": session_id,
        "session_id": session_id,
        "case_id": request.case_id,
        "observation": observation_payload(case),
        "hypotheses": [name for name, _ in registered_experiments[0].updates] if registered_experiments else [],
    }


@app.post("/api/sessions", status_code=201)
def create_session(request: StartInvestigationRequest) -> dict:
    return start_investigation(request)


@app.post("/api/sessions/{session_id}/start")
def session_start(session_id: str) -> dict:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Investigation not found")
    try:
        previous = session["state"]
        session["state"] = transition(session["state"], InvestigationState.INVESTIGATION)
        append_event(session, "STATE", from_state=previous, to_state=session["state"])
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {"session_id": session_id, "case_id": session["case_id"], "status": "IN_PROGRESS", "state": session["state"]}


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
    SESSIONS[session_id] = {"case_id": case_id, "completed": [], "events": [], "state": InvestigationState.BRIEFING.value, "created_at": datetime.now(timezone.utc).isoformat(), "score": 50, "score_events": ["START_INVESTIGATION"], "diagnostic_id": diagnostic_id}
    append_event(SESSIONS[session_id], "RESTART", reason="USER_REQUESTED_RESTART")
    return {"session_id": session_id, "case_id": case_id, "state": InvestigationState.BRIEFING.value, "diagnostic_id": diagnostic_id}


@app.get("/api/sessions/{session_id}/evidence")
def session_evidence(session_id: str, limit: int = Query(default=100, ge=1, le=100), offset: int = Query(default=0, ge=0), business_key: str | None = Query(default=None, max_length=64)) -> dict:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Investigation not found")
    fixture = generate_case(session["case_id"])
    if not session.get("inspected_evidence"):
        session["inspected_evidence"] = True
        session["score"] = min(1000, session.get("score", 0) + 100)
        session.setdefault("score_events", []).append("INSPECT_HIGH_VALUE_EVIDENCE")
        append_event(session, "EVIDENCE_INSPECTED", evidence_scope="CURATED_SOURCE_RECORDS")
    evidence = fixture.curated_projection()["records"]
    if business_key:
        evidence = [item for item in evidence if item["business_key"] == business_key]
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
    session["score"] = max(0, session.get("score", 50) - 50)
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
    session["state"] = transition(session["state"], InvestigationState.VERDICT)
    append_event(session, "STATE", from_state=previous, to_state=session["state"])
    previous = session["state"]
    session["state"] = transition(session["state"], InvestigationState.DEBRIEF)
    append_event(session, "STATE", from_state=previous, to_state=session["state"])
    score = session.get("score", 50)
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
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Investigation not found")
    if session.get("status") == "COMPLETE":
        raise HTTPException(status_code=409, detail="Investigation is complete")
    # Client completion lists are advisory only. The server's session ledger is
    # authoritative, which prevents double-clicks or forged state from
    # repeating/skipping an Experiment.
    completed = list(session.get("completed", []))
    result = next_experiment(ExperimentRequest(case_id=session["case_id"], completed_experiments=completed, player_prediction=request.player_prediction, conversation_id=session.get("conversation_id")))
    session["completed"] = list(dict.fromkeys(completed + [result["experiment_id"]]))
    session["score"] = session.get("score", 50)
    if session["state"] == InvestigationState.BRIEFING.value:
        previous = session["state"]
        session["state"] = transition(session["state"], InvestigationState.INVESTIGATION)
        append_event(session, "STATE", from_state=previous, to_state=session["state"])
    previous = session["state"]
    session["state"] = transition(session["state"], InvestigationState.EXPERIMENT_RESULT)
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
    review_mode = os.getenv("CHALLENGE_REVIEW_MODE", "0") == "1"
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
        except Exception:
            pass
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
    if case.state != "CORE" and os.getenv("CHALLENGE_REVIEW_MODE", "0") != "1":
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
    if not question or len(question) > 2000:
        raise HTTPException(status_code=422, detail="question must be 1-2000 characters")
    return ask_genie(GenieQuestionRequest(case_id=session["case_id"], conversation_id=session.get("conversation_id"), question=question))


DIST = Path(__file__).resolve().parent.parent / "dist"
AXE = Path(__file__).resolve().parent.parent / "node_modules" / "axe-core"
if os.getenv("LOCAL_A11Y_TEST") == "1" and AXE.exists():
    @app.get("/__test__/a11y", response_class=HTMLResponse)
    def local_a11y_harness() -> str:
        bundle = next((DIST / "assets").glob("index-*.js"), None)
        if bundle is None:
            raise HTTPException(status_code=503, detail="frontend bundle is missing")
        return f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"><title>MAD DATA LAB accessibility harness</title><script src="/__test__/axe.min.js"></script></head><body><div id="root"></div><div id="axe-result" role="status">running</div><script type="module" src="/assets/{bundle.name}"></script><script>setTimeout(()=>axe.run().then(r=>document.getElementById("axe-result").textContent=JSON.stringify({{violations:r.violations.map(v=>({{id:v.id,impact:v.impact,nodes:v.nodes.length}})),passes:r.passes.length}})),1500);</script></body></html>'''
    app.mount("/__test__", StaticFiles(directory=AXE), name="local-a11y-test")
if DIST.exists():
    app.mount("/", StaticFiles(directory=DIST, html=True), name="frontend")
