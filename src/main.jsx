import React, { useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";
import "./evidence-polish.css";
import "./accessibility.css";
import {
  askGenie,
  concludeSession,
  getCaseExperiments,
  getNextExperiment,
  getNextSessionExperiment,
  getSessionEvidence,
  submitPrediction,
  requestHint,
  restartSession,
  listCases,
  startInvestigation,
  createSession,
  startSession,
  submitFinalPrediction,
  enterDebrief,
  inspectEvidence,
  getSession,
} from "./api";

const CASES = [];
const INITIAL_CASE = { id: "CASE_0042", number: "042", title: "Loading case…", metric: "", hook: "", difficulty: "", concepts: "", state: "LOADING", expected: 0, observed: 0, deviation: 0 };

const formatMoney = (value) => `${value < 0 ? "-" : ""}€${Math.abs(value).toFixed(1)}M`;

function App() {
  const [screen, setScreen] = useState("board");
  const [exp, setExp] = useState(-1);
  const [prediction, setPrediction] = useState("");
  const [experiment, setExperiment] = useState(null);
  const [completed, setCompleted] = useState([]);
  const [conversationId, setConversationId] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [diagnosticId, setDiagnosticId] = useState(null);
  const [evidenceRecords, setEvidenceRecords] = useState([]);
  const [conclusion, setConclusion] = useState(null);
  const [loading, setLoading] = useState(false);
  const [serviceError, setServiceError] = useState("");
  const [audioOn, setAudioOn] = useState(() => localStorage.getItem("mad-data-lab-audio") === "on");
  const [askOpen, setAskOpen] = useState(false);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [asking, setAsking] = useState(false);
  const [hintsUsed, setHintsUsed] = useState(0);
  const [hintText, setHintText] = useState("");
  const [earnedBadges, setEarnedBadges] = useState(() => {
    try { return JSON.parse(localStorage.getItem("mad-data-lab-badges") || "[]"); }
    catch { return []; }
  });
  const [panel, setPanel] = useState(null);
  const [reducedMotion, setReducedMotion] = useState(() => localStorage.getItem("mad-data-lab-reduced-motion") === "on");
  const [caseCatalog, setCaseCatalog] = useState(CASES);
  const [selectedCaseId, setSelectedCaseId] = useState("CASE_0042");
  const [experimentRegistry, setExperimentRegistry] = useState([]);
  const [finalPrediction, setFinalPrediction] = useState("");
  const [finalStage, setFinalStage] = useState(false);
  const [initialSubmitted, setInitialSubmitted] = useState(false);
  const [inspectedCapabilities, setInspectedCapabilities] = useState([]);
  const recoveryAttempted = useRef(false);
  const audioRef = useRef(null);
  useEffect(() => {
    listCases()
      .then((result) => {
        if (Array.isArray(result.cases) && result.cases.length) {
          CASES.splice(0, CASES.length, ...result.cases);
          setCaseCatalog(result.cases);
          setSelectedCaseId((current) => result.cases.some((item) => item.id === current) ? current : result.cases[0].id);
        }
      })
      .catch(() =>
        setServiceError(
          "Local case catalog active — remote catalog unavailable.",
        ),
      );
  }, []);
  const active = caseCatalog.find((item) => item.id === selectedCaseId) || caseCatalog[0] || INITIAL_CASE;
  // Analytical values come only from the case catalog response.  The loading
  // placeholder intentionally contains zeros and must never become a Case
  // #042 fallback when the API is unavailable.
  const deviation = Number(active.deviation ?? 0);
  const expected = Number(active.expected ?? 0);
  const observed = Number(active.observed ?? 0);
  useEffect(() => {
    getCaseExperiments(active.id).then((result) => {
      if (Array.isArray(result.catalog) && result.catalog.length) {
        setExperimentRegistry(result.catalog);
      }
    }).catch(() => setExperimentRegistry([]));
  }, [active.id]);
  useEffect(() => {
    if (recoveryAttempted.current) return;
    const savedSessionId = localStorage.getItem("mad-data-lab-session-id");
    if (!savedSessionId) { recoveryAttempted.current = true; return; }
    getSession(savedSessionId).then(async (session) => {
      recoveryAttempted.current = true;
      setSelectedCaseId(session.case_id || "CASE_0042");
      setSessionId(savedSessionId);
      setConversationId(session.conversation_id || null);
      setDiagnosticId(session.diagnostic_id || null);
      setPrediction(session.initial_prediction || "");
      setFinalPrediction(session.final_prediction && session.final_prediction !== "SKIPPED_BY_EARLY_REVEAL" ? session.final_prediction : "");
      setInitialSubmitted(Boolean(session.initial_prediction));
      setCompleted(session.completed || []);
      setHintsUsed(Number(session.hints || 0));
      setInspectedCapabilities(session.inspected_capabilities || []);
      const lastExperiment = [...(session.events || [])].reverse().find((event) => event.type === "EXPERIMENT" && event.result);
      if (lastExperiment?.result) {
        setExperiment(lastExperiment.result);
        setExp(Number(lastExperiment.result.experiment_number || 1) - 1);
      }
      if (session.state === "DEBRIEF") {
        setConclusion(session); setScreen("debrief");
      } else if (session.state === "CONCLUDING") {
        setConclusion(session); setScreen("verdict");
      } else {
        setFinalStage(session.state === "PLAYER_PREDICTION_FINAL");
        if (session.state !== "CASE_BRIEFING") setScreen("investigation");
      }
      try {
        const evidenceResult = await getSessionEvidence(savedSessionId);
        setEvidenceRecords(evidenceResult.evidence || []);
      } catch { /* the session projection remains usable without evidence details */ }
    }).catch(() => {
      recoveryAttempted.current = true;
      localStorage.removeItem("mad-data-lab-session-id");
    });
  }, []);
  useEffect(() => {
    document.documentElement.classList.toggle("reduced-motion", reducedMotion);
  }, [reducedMotion]);
  useEffect(() => {
    if (screen !== "debrief" || !conclusion?.badges?.length) return;
    const newBadges = conclusion.badges;
    setEarnedBadges(newBadges);
    localStorage.setItem("mad-data-lab-badges", JSON.stringify(newBadges));
  }, [screen, conclusion]);
  const toggleAudio = () => {
    const audio = audioRef.current;
    if (!audio) return;
    if (audioOn) {
      audio.pause();
      setAudioOn(false);
    } else {
      audio
        .play()
        .then(() => setAudioOn(true))
        .catch(() =>
          setServiceError("Audio playback needs to be allowed by the browser."),
        );
    }
  };
  const start = (caseToOpen = active) => {
    setSelectedCaseId(caseToOpen.id);
    setScreen("briefing");
    setExp(-1);
    setExperiment(null);
    setCompleted([]);
    setConversationId(null);
    setSessionId(null);
    setDiagnosticId(null);
    setEvidenceRecords([]);
    setConclusion(null);
    setPrediction("");
    setFinalPrediction("");
    setFinalStage(false);
    setInitialSubmitted(false);
    setInspectedCapabilities([]);
    setAnswer("");
    setQuestion("");
    setServiceError("");
    setHintsUsed(0);
    setHintText("");
    setInspectedCapabilities([]);
  };
  const showHint = () => {
    if (hintsUsed >= 3) return;
    if (!sessionId) {
      setServiceError("Start an investigation before requesting a hint.");
      return;
    }
    requestHint(sessionId).then((result) => {
      setHintText(result.hint);
      setHintsUsed(result.hint_number);
    }).catch(() => setServiceError("Hints are temporarily unavailable."));
  };
  useEffect(() => {
    localStorage.setItem("mad-data-lab-audio", audioOn ? "on" : "off");
  }, [audioOn]);
  useEffect(() => {
    localStorage.setItem("mad-data-lab-reduced-motion", reducedMotion ? "on" : "off");
  }, [reducedMotion]);
  const begin = async () => {
    setScreen("investigation");
    setLoading(true);
    setServiceError("");
    try {
      const created = await createSession(active.id);
      const createdSessionId = String(created.session_id || "");
      if (createdSessionId) {
        setSessionId(createdSessionId);
        localStorage.setItem("mad-data-lab-session-id", createdSessionId);
      }
      const session = await startSession(createdSessionId);
      setConversationId(session.conversation_id || null);
      setSessionId(session.session_id || session.investigation_id || null);
      localStorage.setItem("mad-data-lab-session-id", session.session_id || session.investigation_id || "");
      setDiagnosticId(session.diagnostic_id || null);
    } catch {
      setServiceError("Investigation service unavailable. Start the API to continue.");
    } finally {
      setLoading(false);
    }
  };
  const run = async () => {
    setLoading(true);
    setServiceError("");
    try {
      if (sessionId && prediction && !initialSubmitted) {
        await submitPrediction(sessionId, prediction);
        setInitialSubmitted(true);
      }
      const next = sessionId
        ? await getNextSessionExperiment(sessionId, prediction)
        : await getNextExperiment(active.id, completed, prediction, conversationId);
      if (next.ready_for_final_prediction) { setFinalStage(true); setExperiment(null); return; }
      setExperiment(next);
      setCompleted((v) => [...v, next.experiment_id]);
      setExp(next.experiment_number - 1);
      if (sessionId) {
        if (next.experiment_id !== "COMPONENT_DECOMPOSITION") {
          const evidenceResult = await getSessionEvidence(sessionId);
          setEvidenceRecords(evidenceResult.evidence || []);
        }
      }
    } catch {
      setServiceError("Dr. Genie is offline. No analytical fallback is available.");
    } finally {
      setLoading(false);
    }
  };
  const revealVerdict = async () => {
    if (sessionId) {
      try {
        if (finalStage && finalPrediction) await submitFinalPrediction(sessionId, finalPrediction);
        const result = await concludeSession(sessionId);
        setConclusion(result);
        setScreen("verdict");
        try {
          const stored = JSON.parse(localStorage.getItem("mad-data-lab-progression") || "{}");
          const completedCaseIds = new Set(stored.completed_case_ids || []);
          completedCaseIds.add(active.id);
          const bestScores = {...(stored.best_scores || {})};
          bestScores[active.id] = Math.max(Number(bestScores[active.id] || 0), Number(result.score || 0));
          localStorage.setItem("mad-data-lab-progression", JSON.stringify({completed_case_ids: [...completedCaseIds], best_scores: bestScores}));
        } catch {
          setServiceError("The server completed the Case; local progression storage is unavailable.");
        }
      } catch {
        setServiceError("The evidence ledger is not complete yet. Run every required experiment.");
        return;
      }
    }
  };
  const openDebrief = async () => {
    if (!sessionId) return;
    try { const result = await enterDebrief(sessionId); setConclusion((current) => ({...current, ...result})); setScreen("debrief"); }
    catch { setServiceError("The Debrief could not be opened yet."); }
  };
  const recoverInvestigation = async () => {
    if (sessionId) {
      try {
        const restarted = await restartSession(sessionId);
        setDiagnosticId(restarted.diagnostic_id || diagnosticId);
      } catch {
        setServiceError("Restart failed. Return to the Case Board and open a new investigation.");
        return;
      }
    }
    setScreen("investigation");
    setExp(-1);
    setExperiment(null);
    setCompleted([]);
    setEvidenceRecords([]);
    setConclusion(null);
    setServiceError("");
  };
  const ask = async () => {
    if (!question.trim()) return;
    setAsking(true);
    setAnswer("");
    try {
      const result = await askGenie(active.id, conversationId, question);
      setAnswer(result.answer);
    } catch {
      setAnswer(
        "Dr. Genie is unavailable right now. Continue with the verified experiments.",
      );
    } finally {
      setAsking(false);
    }
  };
  const inspect = async (capability) => {
    if (!sessionId || inspectedCapabilities.includes(capability)) return;
    try {
      await inspectEvidence(sessionId, capability);
      setInspectedCapabilities((items) => [...items, capability]);
    } catch { setServiceError("That evidence is not unlocked yet."); }
  };
  const current = experiment || (exp >= 0 ? experimentRegistry[exp] : null);
  const updates = current?.hypothesis_updates || current?.updates || [];
  const evidence = current?.evidence || "";
  return (
    <div className="app">
      <audio
        ref={audioRef}
        loop
        preload="none"
        src="/audio/mad_data_lab_curiosity.mp3"
        onError={() => setServiceError("Background music unavailable; gameplay continues.")}
      />
      <header className="topbar">
        <div className="brand">
          <span className="lime">MAD</span> <span className="cyan">DATA</span>{" "}
          <span className="pink">LAB</span>
          <span className="flask">⚗</span>
        </div>
        <div className="case-title">
          CASE FILE: <b>{active.title.toUpperCase()}</b>
          <small>{formatMoney(deviation)} SUSPECTED BUT NOT EXPLAINED</small>
        </div>
        <div className="controls">
          <button aria-label="Help" onClick={() => setPanel("help")}>?</button>
          <button aria-label="Log" onClick={() => setPanel("log")}>▤</button>
          <button aria-label="Settings" onClick={() => setPanel("settings")}>⚙</button>
          <button
            aria-label={
              audioOn ? "Mute laboratory music" : "Play laboratory music"
            }
            onClick={toggleAudio}
          >
            {audioOn ? "🔊" : "♫"}
          </button>
        </div>
      </header>
      {panel && (
        <div className="modal-backdrop" role="presentation" onClick={() => setPanel(null)}>
          <section className="modal-panel" role="dialog" aria-modal="true" aria-labelledby="modal-title" onClick={(event) => event.stopPropagation()}>
            <button className="modal-close" aria-label="Close panel" onClick={() => setPanel(null)}>×</button>
            {panel === "help" && <>
              <p className="eyebrow">FIELD MANUAL</p>
              <h2 id="modal-title">How to investigate</h2>
              <p>Make a prediction, then let Dr. Genie choose the highest-information experiment. Inspect the evidence before accepting a cause.</p>
              <ol><li>Observe the anomaly.</li><li>Test the strongest signal.</li><li>Challenge false leads.</li><li>Reconcile the full deviation.</li></ol>
            </>}
            {panel === "log" && <>
              <p className="eyebrow">INVESTIGATION LOG</p>
              <h2 id="modal-title">Case #{active.number}</h2>
              {completed.length ? <ol>{completed.map((item, index) => <li key={`${item}-${index}`}>{item} completed</li>)}</ol> : <p>No experiments recorded yet. Your log will appear here as Genie investigates.</p>}
            </>}
            {panel === "settings" && <>
              <p className="eyebrow">LAB SETTINGS</p>
              <h2 id="modal-title">Accessibility</h2>
              <label className="setting-row"><span>Reduce motion</span><input type="checkbox" checked={reducedMotion} onChange={(event) => setReducedMotion(event.target.checked)} /></label>
              <p className="setting-note">Animations are shortened while evidence and controls remain unchanged.</p>
            </>}
          </section>
        </div>
      )}
      {serviceError && screen !== "investigation" && (
        <section className="error-panel" role="alert" aria-labelledby="error-title">
          <p className="eyebrow">LAB RECOVERY</p>
          <h2 id="error-title">The investigation needs attention.</h2>
          <p>{serviceError}</p>
          {diagnosticId && <small>Diagnostic ID: {diagnosticId}</small>}
          <div className="error-actions">
            <button className="primary" onClick={recoverInvestigation}>RESTART INVESTIGATION</button>
            <button className="secondary" onClick={() => setScreen("board")}>RETURN TO CASE BOARD</button>
          </div>
        </section>
      )}
      {screen === "board" && (
        <main className="hub">
          <div className="hero">
            <div className="lab-mark" role="img" aria-label="Pixel-art MAD DATA LAB laboratory flask mark" />
            <div className="hero-copy">
              <p className="eyebrow">
                DR. GENIE'S EXPERIMENTAL DATA LABORATORY
              </p>
              <h1>Turn suspicious numbers into explainable experiments.</h1>
              <button className="primary" onClick={start}>
                OPEN CASE BOARD <span>→</span>
              </button>
            </div>
          </div>
          <section className="case-board">
            <div className="section-head">
              <div>
                <p className="eyebrow">CASE BOARD</p>
                <h2>Choose an anomaly to investigate</h2>
              </div>
              <span className="chip">{caseCatalog.filter((item) => (item.availability || item.state) === "AVAILABLE" || item.state === "CORE").length} CASE READY · {earnedBadges.length ? "BADGE EARNED" : "NEW SCIENTIST"}</span>
            </div>
            <div className="cards">
              {caseCatalog.map((c) => (
                <article
                  className={"case-card " + ((c.availability || c.state) === "AVAILABLE" ? "featured" : "locked")}
                  key={c.id}
                >
                  <div className="card-number">CASE #{c.number}</div>
                  <h3>{c.title}</h3>
                  <p>{c.hook}</p>
                  <div className="card-meta">
                    <span>{c.difficulty}</span>
                    <span>{(c.availability || c.state) === "AVAILABLE" ? "●●○" : "LOCKED"}</span>
                  </div>
                  <button
                    className={(c.availability || c.state) === "AVAILABLE" ? "primary" : "secondary"}
                    onClick={(c.availability || c.state) === "AVAILABLE" ? () => start(c) : undefined}
                    disabled={(c.availability || c.state) !== "AVAILABLE"}
                  >
                    {(c.availability || c.state) === "AVAILABLE" ? "OPEN CASE" : "COMING SOON"}
                  </button>
                </article>
              ))}
            </div>
          </section>
        </main>
      )}
      {screen === "briefing" && (
        <main className="briefing">
          <div className="brief-art">
            <div className="lab-visual briefing-visual" role="img" aria-label="Pixel-art Dr. Genie laboratory scientist" />
          </div>
          <div className="brief-panel">
            <p className="eyebrow">
              CASE #{active.number} · {active.difficulty}
            </p>
            <h1>{active.title}</h1>
            <p className="lead">
              Someone expected <strong>{formatMoney(expected)}</strong> in {active.metric}.
              The current snapshot reports <strong>{formatMoney(observed)}</strong>.
            </p>
            <div className="metric">
              <span>DEVIATION</span>
              <strong>{formatMoney(deviation)}</strong>
              <small>
                Find the root cause without trusting the first explanation.
              </small>
            </div>
            <p className="genie-line">
              “Welcome, data detective. Form a theory, then let’s make the
              numbers confess.”
            </p>
            <button className="primary" onClick={begin}>
              START INVESTIGATION <span>→</span>
            </button>
            <button className="text-button" onClick={() => setScreen("board")}>
              ← Back to Case Board
            </button>
          </div>
        </main>
      )}
      {screen === "investigation" && (
        <main className="investigation">
          <section className="stage">
            <div className="stage-image">
              <div className="lab-visual stage-visual" role="img" aria-label="Pixel-art data investigation instrument" />
            </div>
            <div className="overlay">
              <div className="observation">
                <span>ANOMALY-O-METER</span>
                <strong>{formatMoney(deviation)}</strong>
                <small>VERY ANOMALOUS</small>
              </div>
              <div className="instrument">
                <span className="step">{exp < 0 ? "1" : " " + (exp + 1)}</span>
                <p>
                  {exp < 0 ? "START INVESTIGATION" : current.name.toUpperCase()}
                </p>
                {exp >= 0 && (
                  <>
                    <div className="bars">
                      <i style={{ height: "88%" }} />
                      <i style={{ height: "42%" }} />
                      <i style={{ height: "20%" }} />
                      <i style={{ height: "10%" }} />
                    </div>
                    <small>{current.instrument}</small>
                  </>
                )}
              </div>
            </div>
          </section>
          <aside className="side">
            <div className="genie">
              <img className="genie-avatar" src="/assets/pixelart/dr-genie-mdl3.png" alt="Dr. Genie" />
              <div>
                <p className="eyebrow">DR. GENIE</p>
                <p>
                  {exp < 0
                    ? `I see a ${formatMoney(deviation)} anomaly. Let’s separate signal from noise.`
                    : current.rationale}
                </p>
              </div>
            </div>
            {serviceError && (
              <div className="service-error" role="status">
                {serviceError}
              </div>
            )}
            {hintText && <div className="hint-card" role="status"><strong>HINT {hintsUsed}/3</strong><span>{hintText}</span></div>}
            <button
              className="genie-console-toggle"
              onClick={() => setAskOpen((v) => !v)}
              aria-expanded={askOpen}
            >
              ASK DR. GENIE {askOpen ? "−" : "+"}
            </button>
            {askOpen && (
              <section className="genie-console">
                <label htmlFor="genie-question">Ask about the evidence</label>
                <textarea
                  id="genie-question"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="Why should I trust the V2 signal?"
                  rows="3"
                />
                <button
                  className="secondary wide"
                  onClick={ask}
                  disabled={asking}
                >
                  {asking ? "GENIE IS THINKING…" : "SEND QUESTION →"}
                </button>
                {answer && (
                  <p className="genie-answer" role="status">
                    {answer}
                  </p>
                )}
              </section>
            )}
            <div className="progress">
              <div>
                <span>INVESTIGATION</span>
                  <b>{exp < 0 ? 0 : Math.round(((exp + 1) / Math.max(experimentRegistry.length, 1)) * 100)}%</b>
              </div>
              <div className="progress-bar">
                <i
                  style={{ width: `${exp < 0 ? 0 : ((exp + 1) / Math.max(experimentRegistry.length, 1)) * 100}%` }}
                />
              </div>
            </div>
            <h2>HYPOTHESES</h2>
            <div className="hypotheses">
              {(exp < 0 ? (experimentRegistry[0]?.hypothesis_updates || experimentRegistry[0]?.updates || []) : updates || [])
                .map((item) =>
                  Array.isArray(item)
                    ? { name: item[0], status: item[1] }
                    : item,
                )
                .map(({ name, status }) => (
                  <div className="hypothesis" key={name}>
                    <span>{name}</span>
                    <b className={status.toLowerCase()}>{status}</b>
                  </div>
                ))}
            </div>
            {exp >= 0 && (
              <section
                className="evidence-explorer"
                aria-labelledby="evidence-heading"
              >
                <div className="evidence-heading">
                  <h2 id="evidence-heading">EVIDENCE EXPLORER</h2>
                  <span>{current.instrument}</span>
                </div>
                <p>{evidence}</p>
                {evidenceRecords.find((item) => item.business_key === "TX-004291") && (
                  <dl>
                    <div>
                      <dt>BUSINESS KEY</dt>
                      <dd>{evidenceRecords.find((item) => item.business_key === "TX-004291").business_key}</dd>
                    </div>
                    <div>
                      <dt>IMPACT</dt>
                      <dd>{formatMoney(evidenceRecords.find((item) => item.business_key === "TX-004291").impact)}</dd>
                    </div>
                    <div>
                      <dt>SOURCE</dt>
                      <dd>{evidenceRecords.find((item) => item.business_key === "TX-004291").source_table || "curated source record"}</dd>
                    </div>
                  </dl>
                )}
                {evidenceRecords.length > 0 && (
                  <small className="evidence-count" role="status">
                    {evidenceRecords.length} curated source records available in the server ledger.
                  </small>
                )}
                {evidenceRecords.length > 0 && <div className="evidence-actions">
                  <button className="secondary" onClick={() => inspect("CASE_0042:RECORD:TX-004291")} disabled={inspectedCapabilities.includes("CASE_0042:RECORD:TX-004291")}>INSPECT TX-004291 · +100</button>
                  <button className="secondary" onClick={() => inspect("CASE_0042:LINEAGE:V2_SOURCE_PATH")} disabled={inspectedCapabilities.includes("CASE_0042:LINEAGE:V2_SOURCE_PATH")}>OPEN V2 LINEAGE · +75</button>
                  <button className="secondary" onClick={() => inspect("CASE_0042:DQ:MATERIALITY")} disabled={inspectedCapabilities.includes("CASE_0042:DQ:MATERIALITY")}>INSPECT DQ MATERIALITY</button>
                </div>}
              </section>
            )}
            {exp >= 0 && current && (
              <section className="experiment-rationale" aria-labelledby="experiment-rationale-heading">
                <h2 id="experiment-rationale-heading">WHY THIS EXPERIMENT?</h2>
                <p>{current.question || "This registered Experiment tests the next allowed evidence claim."}</p>
                <dl>
                  <div><dt>INSTRUMENT</dt><dd>{current.instrument || "Registered evidence instrument"}</dd></div>
                  {current.target && <div><dt>TARGET</dt><dd>{current.target}</dd></div>}
                </dl>
              </section>
            )}
            <div className="prediction">
              <label htmlFor="prediction-choice">Your prediction</label>
              <select
                id="prediction-choice"
                value={prediction}
                onChange={(e) => setPrediction(e.target.value)}
              >
                <option value="">What is most likely?</option>
                <option value="PRED_SOURCE_VALUES_CHANGED">Component movement</option>
                <option value="PRED_DATA_QUALITY_PRIMARY">Data quality issue</option>
                <option value="PRED_FORMULA_CHANGED">Formula change</option>
                <option value="PRED_INSUFFICIENT_EVIDENCE">Insufficient evidence</option>
              </select>
            </div>
            {finalStage ? (
              <>
                <label htmlFor="final-prediction">FINAL PREDICTION</label>
                <select id="final-prediction" value={finalPrediction} onChange={(e) => setFinalPrediction(e.target.value)}>
                  <option value="">Choose the evidence-grounded conclusion</option>
                  <option value="FINAL_CHANGED_V2_SOURCE_RECORDS">Changed V2 source records</option>
                  <option value="FINAL_DATA_QUALITY_PRIMARY">Primary data quality issue</option>
                  <option value="FINAL_FORMULA_CHANGED">Formula changed</option>
                  <option value="FINAL_INSUFFICIENT_EVIDENCE">Insufficient evidence</option>
                </select>
                <button className="primary wide" onClick={revealVerdict} disabled={!finalPrediction || loading}>ACCEPT SCIENTIFIC VERDICT <span>→</span></button>
                <button className="text-button wide" onClick={async () => {
                  if (!window.confirm("Reveal now and skip the final prediction? This costs 150 points.")) return;
                  try { const result = await concludeSession(sessionId, {mode: "EARLY_REVEAL"}); setConclusion(result); setScreen("verdict"); }
                  catch { setServiceError("Early reveal is available only after all analytical requirements are complete."); }
                }}>REVEAL NOW · SKIP FINAL PREDICTION (-150)</button>
              </>
            ) : experimentRegistry.length > 0 && exp < experimentRegistry.length - 1 ? (
              <button className="primary wide" onClick={run} disabled={loading}>
                {loading
                  ? "GENIE IS INVESTIGATING…"
                  : exp < 0
                    ? "RUN GENIE’S FIRST EXPERIMENT"
                    : "RUN NEXT EXPERIMENT"}{" "}
                <span>→</span>
              </button>
            ) : experimentRegistry.length > 0 ? (
              <button
                className="primary wide"
                onClick={run}
                disabled={loading}
              >
                {loading ? "PREPARING FINAL PREDICTION…" : "CONTINUE TO FINAL PREDICTION"} <span>→</span>
              </button>
            ) : (
              <button className="primary wide" disabled>No experiment contract available</button>
            )}
            <button className="text-button" onClick={() => setScreen("board")}>
              Exit Investigation
            </button>
            <button className="text-button hint-button" onClick={showHint} disabled={hintsUsed >= 3}>
              {hintsUsed >= 3 ? "ALL HINTS USED" : `SHOW HINT · ${3 - hintsUsed} REMAINING`}
            </button>
          </aside>
        </main>
      )}
      {screen === "verdict" && (
        <main className="verdict">
          <div className="verdict-card">
            <p className="eyebrow">
              SCIENTIFIC VERDICT · CASE #{active.number}
            </p>
            <h1>{conclusion?.verdict || "The server has not issued a scientific verdict."}</h1>
            <p className="lead">
              The evidence reconciles the full <strong>{formatMoney(deviation)}</strong>{" "}
              deviation for <strong>{active.title}</strong>. The investigation
              completed its registered experiments and recorded the evidence.
            </p>
            <div className="verdict-grid">
              <div>
                <span>CONFIDENCE</span>
                <strong>HIGH</strong>
              </div>
              <div>
                <span>RECONCILIATION</span>
                <strong>€0.0M UNEXPLAINED</strong>
              </div>
              <div>
                <span>FALSE LEAD</span>
                <strong>{conclusion?.false_lead || "SERVER-RECORDED EVIDENCE"}</strong>
              </div>
            </div>
            <p className="genie-line">
              “Excellent work. A warning can be real without being the root
              cause. Follow the evidence.”
            </p>
            <button className="primary" onClick={openDebrief}>
              OPEN DEBRIEF <span>→</span>
            </button>
          </div>
        </main>
      )}
      {screen === "debrief" && (
        <main className="verdict">
          <div className="verdict-card debrief-card">
            <p className="eyebrow">
              INVESTIGATION COMPLETE · CASE #{active.number}
            </p>
            <h1>Junior Metric Scientist: certified.</h1>
            <div className="score">
              <span>LAB SCORE</span>
              <strong>{conclusion?.score ?? 0}</strong>
              <small>
                {conclusion?.score_events?.length
                  ? "Evidence ledger recorded · Reconciled conclusion"
                  : "Server score unavailable"}
              </small>
            </div>
            <div className="badges" aria-label="Earned badges">
              <span className="eyebrow">BADGES</span>
              {earnedBadges.length ? earnedBadges.map((badge) => <strong key={badge}>✦ {badge}</strong>) : <small>Complete the investigation to earn your first badges.</small>}
            </div>
            <div className="debrief-grid">
              <div>
                <span>CONCEPT 01</span>
                <strong>Baseline first</strong>
                <p>
                  Compare observed values with an expectation before explaining
                  the anomaly.
                </p>
              </div>
              <div>
                <span>CONCEPT 02</span>
                <strong>Test the largest signal</strong>
                <p>
                  Genie selected the next experiment from the registered Case
                  contract and followed the strongest available signal.
                </p>
              </div>
              <div>
                <span>CONCEPT 03</span>
                <strong>Quality is not causality</strong>
                <p>
                  A real warning or competing signal is tested before causality
                  is accepted.
                </p>
              </div>
            </div>
            <button className="primary" onClick={() => setScreen("board")}>
              RETURN TO CASE BOARD <span>→</span>
            </button>
            <button
              className="text-button"
              onClick={() => {
                setScreen("briefing");
                setExp(-1);
                setExperiment(null);
                setCompleted([]);
                setPrediction("");
                setHintsUsed(0);
                setHintText("");
              }}
            >
              REPLAY CASE
            </button>
          </div>
        </main>
      )}
    </div>
  );
}
createRoot(document.getElementById("root")).render(<App />);
