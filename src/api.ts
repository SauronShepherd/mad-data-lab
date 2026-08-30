export type CaseId = `CASE_${number}`;
export type ExperimentResult = {
  case_id: string; experiment_id: string; experiment_number: number;
  name: string; instrument: string; rationale: string; evidence: string;
  hypothesis_updates: Array<{name: string; status: string}>; source?: string;
};
export type EvidenceRecord = { business_key: string; impact: number; [key: string]: unknown };
type Json = Record<string, unknown>;
const API_BASE = import.meta.env.VITE_API_BASE || (import.meta.env.DEV ? 'http://localhost:8000' : '');

const SCIENCE_GLITCHES = [
  "Something went gloriously sideways. It’s not you, it’s me — the data goblins are recalibrating the moon.",
  "The lab sneezed on the pipeline. It’s not you, it’s me — a tiny robot is putting the rows back in order.",
  "Our Genie briefly escaped into a spreadsheet. It’s not you, it’s me — please try the experiment again.",
  "The numbers have formed a union. It’s not you, it’s me — the lab is negotiating with a rebellious chart.",
];

const publicErrorMessage = (code?: string, fallback?: string) => {
  if (["SESSION_EXPIRED", "INVALID_REQUEST", "DUPLICATE_ACTION", "ALL_EXPERIMENTS_COMPLETE"].includes(code || "")) return fallback;
  return SCIENCE_GLITCHES[Math.floor(Math.random() * SCIENCE_GLITCHES.length)];
};

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, init);
  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    const error = payload?.error;
    const failure = new Error(publicErrorMessage(error?.code, error?.message || `API request failed: ${response.status}`)) as Error & { code?: string; retryable?: boolean; requestId?: string; technicalMessage?: string };
    failure.code = error?.code; failure.retryable = error?.retryable; failure.requestId = error?.request_id;
    failure.technicalMessage = error?.message;
    throw failure;
  }
  return response.json() as Promise<T>;
}
const post = <T>(path: string, body: Json, idempotencyKey?: string): Promise<T> => request<T>(path, {method: 'POST', headers: {'Content-Type': 'application/json', ...(idempotencyKey ? {'Idempotency-Key': idempotencyKey} : {})}, body: JSON.stringify(body)});
const sessionPost = <T>(path: string, body: Json = {}) => post<T>(path, body, crypto.randomUUID());

export const listCases = () => request<{cases: Json[]}>('/api/cases');
export const getCaseExperiments = (caseId: string) => request<{catalog: ExperimentResult[]; experiments: string[]}>(`/api/cases/${encodeURIComponent(caseId)}/experiments`);
export const startInvestigation = (caseId: string) => post<Json>('/api/investigations', {case_id: caseId});
export const createSession = (caseId: string) => post<Json>('/api/sessions', {case_id: caseId}, crypto.randomUUID());
export const startSession = (sessionId: string) => sessionPost<Json>(`/api/sessions/${encodeURIComponent(sessionId)}/start`);
export const getNextExperiment = (caseId: string, completedExperiments: string[], playerPrediction?: string, conversationId?: string | null) => post<ExperimentResult>('/api/experiments/next', {case_id: caseId, completed_experiments: completedExperiments, player_prediction: playerPrediction || null, conversation_id: conversationId || null});
export const getNextSessionExperiment = (sessionId: string, playerPrediction?: string) => sessionPost<ExperimentResult>(`/api/sessions/${encodeURIComponent(sessionId)}/next`, {player_prediction: playerPrediction || null});
export const getSessionEvidence = (sessionId: string) => request<{evidence: EvidenceRecord[]}>(`/api/sessions/${encodeURIComponent(sessionId)}/evidence?limit=100`);
export const concludeSession = (sessionId: string, body: Json = {}) => sessionPost<Json>(`/api/sessions/${encodeURIComponent(sessionId)}/conclude`, body);
export const submitPrediction = (sessionId: string, prediction: string) => sessionPost<Json>(`/api/sessions/${encodeURIComponent(sessionId)}/prediction`, {prediction});
export const requestHint = (sessionId: string) => sessionPost<{hint: string; hint_number: number}>(`/api/sessions/${encodeURIComponent(sessionId)}/hint`, {});
export const restartSession = (sessionId: string) => post<Json>(`/api/sessions/${encodeURIComponent(sessionId)}/restart`, {});
export const getSession = (sessionId: string) => request<Json>(`/api/sessions/${encodeURIComponent(sessionId)}`);
export const inspectEvidence = (sessionId: string, capability: string) => sessionPost<Json>(`/api/sessions/${encodeURIComponent(sessionId)}/evidence/inspect`, {capability});
export const submitFinalPrediction = (sessionId: string, prediction: string) => sessionPost<Json>(`/api/sessions/${encodeURIComponent(sessionId)}/prediction`, {prediction, final: true});
export const enterDebrief = (sessionId: string) => sessionPost<Json>(`/api/sessions/${encodeURIComponent(sessionId)}/debrief`);
export const askGenie = (caseId: string, conversationId: string | null, question: string) => post<{answer: string}>(`/api/genie/ask`, {case_id: caseId, conversation_id: conversationId, question});
