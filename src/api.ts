export type CaseId = `CASE_${number}`;
export type ExperimentResult = {
  case_id: string; experiment_id: string; experiment_number: number;
  name: string; instrument: string; rationale: string; evidence: string;
  hypothesis_updates: Array<{name: string; status: string}>; source?: string;
};
export type EvidenceRecord = { business_key: string; impact: number; [key: string]: unknown };
type Json = Record<string, unknown>;
const API_BASE = import.meta.env.VITE_API_BASE || (import.meta.env.DEV ? 'http://localhost:8000' : '');

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, init);
  if (!response.ok) throw new Error(`API request failed: ${response.status}`);
  return response.json() as Promise<T>;
}
const post = <T>(path: string, body: Json): Promise<T> => request<T>(path, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)});

export const listCases = () => request<{cases: Json[]}>('/api/cases');
export const getCaseExperiments = (caseId: string) => request<{catalog: ExperimentResult[]; experiments: string[]}>(`/api/cases/${encodeURIComponent(caseId)}/experiments`);
export const startInvestigation = (caseId: string) => post<Json>('/api/investigations', {case_id: caseId});
export const getNextExperiment = (caseId: string, completedExperiments: string[], playerPrediction?: string, conversationId?: string | null) => post<ExperimentResult>('/api/experiments/next', {case_id: caseId, completed_experiments: completedExperiments, player_prediction: playerPrediction || null, conversation_id: conversationId || null});
export const getNextSessionExperiment = (sessionId: string, playerPrediction?: string) => post<ExperimentResult>(`/api/sessions/${encodeURIComponent(sessionId)}/next`, {player_prediction: playerPrediction || null});
export const getSessionEvidence = (sessionId: string) => request<{evidence: EvidenceRecord[]}>(`/api/sessions/${encodeURIComponent(sessionId)}/evidence?limit=100`);
export const concludeSession = (sessionId: string) => post<Json>(`/api/sessions/${encodeURIComponent(sessionId)}/conclude`, {});
export const submitPrediction = (sessionId: string, prediction: string) => post<Json>(`/api/sessions/${encodeURIComponent(sessionId)}/prediction`, {prediction});
export const requestHint = (sessionId: string) => post<{hint: string; hint_number: number}>(`/api/sessions/${encodeURIComponent(sessionId)}/hint`, {});
export const restartSession = (sessionId: string) => post<Json>(`/api/sessions/${encodeURIComponent(sessionId)}/restart`, {});
export const askGenie = (caseId: string, conversationId: string | null, question: string) => post<{answer: string}>(`/api/genie/ask`, {case_id: caseId, conversation_id: conversationId, question});
