import React, { useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";
import "./styles/tokens.css";
import "./accessibility.css";
import { InstrumentRenderer } from "./instruments.jsx";
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
const instrumentAlias = (value) => ({
  component_evidence: "WATERFALL",
  snapshot_evidence: "SNAPSHOT_DIFF",
  dq_evidence: "DQ_PANEL",
  formula_evidence: "FORMULA_CHECK",
  reconciliation_evidence: "RECONCILIATION",
}[value] || value);
const readableEvidence = (value) => {
  if (typeof value !== "string") return value || "Curated evidence returned by the live Genie query.";
  try {
    const parsed = JSON.parse(value);
    return typeof parsed === "string" ? parsed : "Curated evidence is available in the instrument and inspection controls below.";
  } catch { return value; }
};

function App() {
  const [screen, setScreen] = useState("landing");
  const [exp, setExp] = useState(-1);
  const [prediction, setPrediction] = useState("");
  const [predictionNotice, setPredictionNotice] = useState("");
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
  const [language, setLanguage] = useState(() => localStorage.getItem("mad-data-lab-language") || "en");
  const [theme, setTheme] = useState(() => localStorage.getItem("mad-data-lab-theme") || "lab");
  const [reducedMotion, setReducedMotion] = useState(() => localStorage.getItem("mad-data-lab-reduced-motion") === "on");
  const [caseCatalog, setCaseCatalog] = useState(CASES);
  const [catalogLoading, setCatalogLoading] = useState(true);
  const [selectedCaseId, setSelectedCaseId] = useState("CASE_0042");
  const [experimentRegistry, setExperimentRegistry] = useState([]);
  const [finalPrediction, setFinalPrediction] = useState("");
  const [finalStage, setFinalStage] = useState(false);
  const [initialSubmitted, setInitialSubmitted] = useState(false);
  const [inspectedCapabilities, setInspectedCapabilities] = useState([]);
  const recoveryAttempted = useRef(false);
  const audioRef = useRef(null);
  const modalRef = useRef(null);
  const publicScreens = new Set(["library", "articles", "groups", "variants", "feedback", "comments", "account", "admin"]);
  useEffect(() => {
    const fromPath = window.location.pathname.replace(/^\//, "");
    if (publicScreens.has(fromPath)) setScreen(fromPath);
    const onPop = () => {
      const path = window.location.pathname.replace(/^\//, "");
      setScreen(publicScreens.has(path) ? path : "board");
    };
    window.addEventListener("popstate", onPop);
    return () => window.removeEventListener("popstate", onPop);
  }, []);
  const goPublic = (path) => {
    const landing = path === "board";
    window.history.pushState({}, "", landing ? "/" : `/${path}`);
    setScreen(landing ? "landing" : path);
    setPanel(null);
  };
  const persistLanguage = (value) => { setLanguage(value); localStorage.setItem("mad-data-lab-language", value); };
  const persistTheme = (value) => { setTheme(value); localStorage.setItem("mad-data-lab-theme", value); };
  const publicCopy = language === "es" ? {
    archive: "MAD DATA LAB · ARCHIVO PÚBLICO",
    returnToLab: "VOLVER AL LABORATORIO",
    articlesTitle: "Artículos de la comunidad",
    articlesIntro: "Lee la historia del laboratorio, el protocolo de Genie y las decisiones de diseño basadas en evidencias.",
    articleTitle: "Maravilloso. Algo no cuadra.",
    articleBody: "Convierte números inesperados en investigaciones científicas reproducibles.",
    libraryTitle: "Biblioteca de evidencias", libraryIntro: "Explora los instrumentos analíticos, conceptos y casos reproducibles del laboratorio.", browseGroups: "EXPLORAR GRUPOS", caseVariants: "VARIANTES DEL CASO",
    groupsTitle: "Grupos de casos", groupsIntro: "Los casos se organizan por la pregunta analítica que enseñan.", groupBody: "Investigaciones guiadas por evidencias.",
    variantsTitle: "Variantes del caso", variantsIntro: "Las variantes son versiones controladas del contrato del caso.", canonical: "CASE #042 · Canónico", canonicalBody: "Datos sintéticos deterministas, cinco experimentos registrados y evidencia autoritativa del servidor.", openBoard: "ABRIR TABLERO DEL CASO",
    feedbackTitle: "Comentarios", feedbackIntro: "Cuéntanos qué ayudó y qué se interpuso.", message: "Mensaje", sendFeedback: "ENVIAR COMENTARIOS", feedbackSaved: "Comentarios guardados localmente durante esta sesión.",
    commentsTitle: "Comentarios de la investigación", commentsIntro: "Deja una nota local sobre el caso mientras revisas la evidencia.", comment: "Comentario", postComment: "PUBLICAR COMENTARIO", commentSaved: "Comentario guardado localmente durante esta sesión.",
    accountTitle: "Cuenta y suscripción", accountIntro: "El progreso y las preferencias se guardan localmente en esta versión candidata.", language: "Idioma", theme: "Tema", manageSubscription: "GESTIONAR SUSCRIPCIÓN", subscriptionDisabled: "El checkout de suscripción no está habilitado en esta versión candidata local.",
    adminTitle: "Administración", adminIntro: "Diagnósticos de release y visibilidad controlada del catálogo.",
  } : {
    archive: "MAD DATA LAB · PUBLIC ARCHIVE",
    returnToLab: "RETURN TO LAB",
    articlesTitle: "Community Articles",
    articlesIntro: "Read the laboratory story, the Genie protocol and the evidence-first design decisions.",
    articleTitle: "Wonderful. Something Is Wrong.",
    articleBody: "Turn unexpected numbers into reproducible scientific investigations.",
    libraryTitle: "Evidence Library", libraryIntro: "Explore the analytical instruments, concepts and reproducible Cases behind the laboratory.", browseGroups: "BROWSE GROUPS", caseVariants: "CASE VARIANTS",
    groupsTitle: "Case Groups", groupsIntro: "Cases are organized by the analytical question they teach.", groupBody: "Evidence-led investigations in this group.",
    variantsTitle: "Case Variants", variantsIntro: "Variants are controlled releases of a Case contract.", canonical: "CASE #042 · Canonical", canonicalBody: "Deterministic synthetic data, five registered experiments and server-authoritative evidence.", openBoard: "OPEN CASE BOARD",
    feedbackTitle: "Feedback", feedbackIntro: "Tell the lab team what helped or got in the way.", message: "Message", sendFeedback: "SEND FEEDBACK", feedbackSaved: "Feedback saved locally for this session.",
    commentsTitle: "Investigation Comments", commentsIntro: "Leave a local note on the current Case while reviewing evidence.", comment: "Comment", postComment: "POST COMMENT", commentSaved: "Comment saved locally for this session.",
    accountTitle: "Account & Subscription", accountIntro: "Progress and preferences are stored locally in this release candidate.", language: "Language", theme: "Theme", manageSubscription: "MANAGE SUBSCRIPTION", subscriptionDisabled: "Subscription checkout is not enabled in this local release candidate.",
    adminTitle: "Administration", adminIntro: "Release diagnostics and controlled catalog visibility.",
  };
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
      )
      .finally(() => setCatalogLoading(false));
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
    }).catch((error) => {
      recoveryAttempted.current = true;
      const code = error?.code;
      if (code === "SESSION_EXPIRED") {
        setSessionId(savedSessionId);
        setServiceError("This investigation expired. Restart it to continue safely.");
      } else {
        localStorage.removeItem("mad-data-lab-session-id");
      }
    });
  }, []);
  useEffect(() => {
    document.documentElement.classList.toggle("reduced-motion", reducedMotion);
  }, [reducedMotion]);
  useEffect(() => {
    if (!panel) return undefined;
    const dialog = modalRef.current;
    if (!dialog) return undefined;
    const focusable = () => [...dialog.querySelectorAll("button, input, select, textarea, [tabindex]:not([tabindex='-1'])")].filter((item) => !item.disabled);
    const initialFocus = window.setTimeout(() => focusable()[0]?.focus(), 0);
    const trap = (event) => {
      if (event.key === "Escape") { setPanel(null); return; }
      if (event.key !== "Tab") return;
      const items = focusable();
      if (!items.length) return;
      const first = items[0];
      const last = items[items.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    };
    document.addEventListener("keydown", trap, true);
    return () => { window.clearTimeout(initialFocus); document.removeEventListener("keydown", trap, true); };
  }, [panel]);
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
      // Persist the user's intent immediately. Browsers may reject playback
      // until a gesture/permission is available, but that must not make the
      // control appear inert or lose the preference.
      setAudioOn(true);
      audio
        .play()
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
      // Load the registered experiment contract before releasing the briefing
      // loading state. This prevents a transient disabled "No experiment
      // contract available" control on slow authenticated deployments.
      const registry = await getCaseExperiments(active.id);
      if (Array.isArray(registry.catalog)) setExperimentRegistry(registry.catalog);
    } catch {
      setServiceError("Investigation service unavailable. Start the API to continue.");
    } finally {
      setLoading(false);
    }
  };
  const run = async () => {
    if (loading) return;
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
      } catch (error) {
        // Preserve the server's actionable completion detail (for example the
        // missing evidence action) instead of masking every 409/422 as a
        // generic Genie failure. This lets the player recover without
        // guessing which requirement is still pending.
        const message = error?.message;
        setServiceError(message || "The evidence ledger is not complete yet. Run every required experiment.");
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
        // The API creates a new session on recovery. Keep the client aligned
        // with that identity; continuing with the expired session makes the
        // next experiment look like a Genie outage to the player.
        const restartedSessionId = String(restarted.session_id || "");
        if (restartedSessionId) {
          setSessionId(restartedSessionId);
          localStorage.setItem("mad-data-lab-session-id", restartedSessionId);
        }
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
          <button className="nav-link" aria-label="Library" onClick={() => goPublic("library")}>LIBRARY</button>
          <button className="nav-link" aria-label="Articles" onClick={() => goPublic("articles")}>ARTICLES</button>
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
          <section ref={modalRef} className="modal-panel" role="dialog" aria-modal="true" aria-labelledby="modal-title" onClick={(event) => event.stopPropagation()}>
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
      {serviceError && (
        <section className="error-panel mdl6-recovery-state" role="alert" aria-labelledby="error-title">
          <img className="mdl6-recovery-art" src="/assets/pixelart/lab-glitch-shrug.png" alt="" aria-hidden="true" />
          <p className="eyebrow">LAB RECOVERY</p>
          <h2 id="error-title">The lab has entered silly mode.</h2>
          <p>{serviceError}</p>
          {diagnosticId && <small>Diagnostic ID: {diagnosticId}</small>}
          <div className="error-actions">
            <button className="primary" onClick={recoverInvestigation}>RESTART INVESTIGATION</button>
            <button className="secondary" onClick={() => setScreen("board")}>RETURN TO CASE BOARD</button>
          </div>
        </section>
      )}
      {publicScreens.has(screen) && <main className="hub public-hub">
        <div className="public-hub-header"><p className="eyebrow">{publicCopy.archive}</p><button className="text-button" onClick={() => goPublic("board")}>{publicCopy.returnToLab}</button></div>
        {screen === "library" && <><h1>{publicCopy.libraryTitle}</h1><p>{publicCopy.libraryIntro}</p><div className="cards"><button className="primary" onClick={() => goPublic("groups")}>{publicCopy.browseGroups}</button><button className="secondary" onClick={() => goPublic("variants")}>{publicCopy.caseVariants}</button></div></>}
        {screen === "articles" && <><h1>{publicCopy.articlesTitle}</h1><p>{publicCopy.articlesIntro}</p><article className="case-card featured"><h2>{publicCopy.articleTitle}</h2><p>{publicCopy.articleBody}</p></article></>}
        {screen === "groups" && <><h1>{publicCopy.groupsTitle}</h1><p>{publicCopy.groupsIntro}</p><div className="cards">{["Decomposition", "Snapshots", "Data quality", "Lineage"].map((item) => <article className="case-card" key={item}><h2>{item}</h2><p>{publicCopy.groupBody}</p></article>)}</div></>}
        {screen === "variants" && <><h1>{publicCopy.variantsTitle}</h1><p>{publicCopy.variantsIntro}</p><article className="case-card featured"><h2>{publicCopy.canonical}</h2><p>{publicCopy.canonicalBody}</p><button className="primary" onClick={() => goPublic("board")}>{publicCopy.openBoard}</button></article></>}
        {screen === "feedback" && <><h1>{publicCopy.feedbackTitle}</h1><p>{publicCopy.feedbackIntro}</p><form onSubmit={(event) => { event.preventDefault(); const text = event.currentTarget.elements["feedback-message"].value.trim(); localStorage.setItem("mad-data-lab-feedback", "saved"); localStorage.setItem("mad-data-lab-feedback-text", text); setServiceError(publicCopy.feedbackSaved); }}><label htmlFor="feedback-message">{publicCopy.message}</label><textarea id="feedback-message" required rows="5" /><button className="primary" type="submit">{publicCopy.sendFeedback}</button></form></>}
        {screen === "comments" && <><h1>{publicCopy.commentsTitle}</h1><p>{publicCopy.commentsIntro}</p><form onSubmit={(event) => { event.preventDefault(); const text = event.currentTarget.elements["comment-message"].value.trim(); localStorage.setItem("mad-data-lab-comment", "saved"); localStorage.setItem("mad-data-lab-comment-text", text); setServiceError(publicCopy.commentSaved); }}><label htmlFor="comment-message">{publicCopy.comment}</label><textarea id="comment-message" required rows="5" /><button className="primary" type="submit">{publicCopy.postComment}</button></form></>}
        {screen === "account" && <><h1>{publicCopy.accountTitle}</h1><p>{publicCopy.accountIntro}</p><label className="setting-row"><span>{publicCopy.language}</span><select value={language} onChange={(event) => persistLanguage(event.target.value)}><option value="en">English</option><option value="es">Español</option></select></label><label className="setting-row"><span>{publicCopy.theme}</span><select value={theme} onChange={(event) => persistTheme(event.target.value)}><option value="lab">Lab dark</option><option value="high-contrast">High contrast</option></select></label><button className="secondary" onClick={() => setServiceError(publicCopy.subscriptionDisabled)}>{publicCopy.manageSubscription}</button></>}
        {screen === "admin" && <><h1>{publicCopy.adminTitle}</h1><p>{publicCopy.adminIntro}</p><pre>{JSON.stringify({cases: caseCatalog.length, badges: earnedBadges.length, theme, language}, null, 2)}</pre></>}
      </main>}
      {(screen === "landing" || screen === "board") && (
        <main className="hub">
          <div className="hero">
            <img className="hero-art" src="/assets/Mad_Data_Lab.png" alt="MAD DATA LAB pixel-art laboratory" />
            <div className="lab-mark" role="img" aria-label="Pixel-art MAD DATA LAB laboratory flask mark" />
            <div className="hero-copy">
              <p className="eyebrow">
                DR. GENIE'S EXPERIMENTAL DATA LABORATORY
              </p>
              <h1>Turn suspicious numbers into explainable experiments.</h1>
              {screen === "landing" && <button className="primary" aria-label="OPEN CASE BOARD" onClick={() => setScreen("board")}>
                OPEN CASE BOARD <span>→</span>
              </button>}
            </div>
          </div>
          <section className="case-board">
            <div className="section-head">
              <div>
                <p className="eyebrow">CASE BOARD</p>
                <h2>Choose an anomaly to investigate</h2>
              </div>
              <span className="chip">{catalogLoading ? "LOADING CASES…" : `${caseCatalog.filter((item) => (item.availability || item.state) === "AVAILABLE" || item.state === "CORE").length} CASE READY · ${earnedBadges.length ? "BADGE EARNED" : "NEW SCIENTIST"}`}</span>
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
            <button className="primary" onClick={begin}>
              START INVESTIGATION <span>→</span>
            </button>
            <div className="metric">
              <span>DEVIATION</span>
              <strong>{formatMoney(deviation)}</strong>
              <small>
                Find the supported explanation without trusting the first hypothesis.
              </small>
            </div>
            <p className="genie-line">
              “Welcome, data detective. Form a theory, then let’s make the
              numbers confess.”
            </p>
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
                <p>
                  {exp < 0 ? "START INVESTIGATION" : current.name.toUpperCase()}
                </p>
                {exp >= 0 && <InstrumentRenderer id={instrumentAlias(current.instrument)} model={{...(current.instrument_model || {}), expected, observed, deviation, records: evidenceRecords.length ? evidenceRecords : (current.instrument_model || {}).records}} />}
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
            <div className="investigation-map" aria-label="State-driven investigation map">
              <div className="map-heading"><span>INVESTIGATION MAP</span><small>Authoritative evidence state</small></div>
              <div className="map-nodes">
                {experimentRegistry.map((node) => {
                  const nodeState = node.status === "RULED_OUT"
                    ? "ruled-out"
                    : completed.includes(node.experiment_id)
                    ? "completed"
                    : current?.experiment_id === node.experiment_id
                      ? "current"
                      : finalStage
                        ? "available"
                        : "locked";
                  return <div className={`map-node ${nodeState}`} key={node.experiment_id} aria-current={nodeState === "current" ? "step" : undefined}>
                    <span className="map-node-state">{nodeState}</span>
                    <strong>{node.name}</strong>
                    <small>{node.instrument}</small>
                  </div>;
                })}
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
                  <span>{instrumentAlias(current.instrument)}</span>
                </div>
                <p>{readableEvidence(evidence)}</p>
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
                  <div><dt>INSTRUMENT</dt><dd>{instrumentAlias(current.instrument) || "Registered evidence instrument"}</dd></div>
                  {current.target && <div><dt>TARGET</dt><dd>{current.target}</dd></div>}
                </dl>
              </section>
            )}
            <div className="prediction">
              <label htmlFor="prediction-choice">Your prediction</label>
              <select
                id="prediction-choice"
                value={prediction}
                className={prediction ? "prediction-selected" : ""}
                onChange={(e) => {
                  const value = e.target.value;
                  setPrediction(value);
                  if (!value) {
                    setPredictionNotice("");
                    return;
                  }
                  const label = e.target.options[e.target.selectedIndex].text;
                  setPredictionNotice(`Hypothesis locked: ${label}`);
                  window.setTimeout(() => setPredictionNotice(""), 4200);
                }}
              >
                <option value="">What is most likely?</option>
                <option value="PRED_SOURCE_VALUES_CHANGED">Component movement</option>
                <option value="PRED_DATA_QUALITY_PRIMARY">Data quality issue</option>
                <option value="PRED_FORMULA_CHANGED">Formula change</option>
                <option value="PRED_INSUFFICIENT_EVIDENCE">Insufficient evidence</option>
              </select>
              {predictionNotice && <div className="prediction-toast" role="status">{predictionNotice}</div>}
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
              <img className="mdl6-badge-art" src="/assets/mdl6-achievement-badges.png" alt="MDL-6 achievement badges: resilience, accessibility, security, and performance" />
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
                localStorage.removeItem("mad-data-lab-session-id");
                start(active);
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
