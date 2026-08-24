const API_BASE = import.meta.env.VITE_API_BASE || (import.meta.env.DEV ? 'http://localhost:8000' : '');

export async function listCases() {
  const response = await fetch(`${API_BASE}/api/cases`);
  if (!response.ok) throw new Error('Case catalog unavailable');
  return response.json();
}

export async function getCaseExperiments(caseId) {
  const response = await fetch(`${API_BASE}/api/cases/${caseId}/experiments`);
  if (!response.ok) throw new Error("Experiment catalog unavailable");
  return response.json();
}

export async function startInvestigation(caseId) {
  const response = await fetch(`${API_BASE}/api/investigations`, {
    method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({case_id: caseId})
  });
  if (!response.ok) throw new Error('Investigation service unavailable');
  return response.json();
}

export async function getNextExperiment(caseId, completedExperiments, playerPrediction, conversationId) {
  const response = await fetch(`${API_BASE}/api/experiments/next`, {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({case_id: caseId, completed_experiments: completedExperiments, player_prediction: playerPrediction || null, conversation_id: conversationId || null})
  });
  if (!response.ok) throw new Error('Experiment service unavailable');
  return response.json();
}

export async function getNextSessionExperiment(sessionId, playerPrediction) {
  const response = await fetch(`${API_BASE}/api/sessions/${sessionId}/next`, {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({player_prediction: playerPrediction || null})
  });
  if (!response.ok) throw new Error('Session experiment service unavailable');
  return response.json();
}

export async function getSessionEvidence(sessionId) {
  const response = await fetch(`${API_BASE}/api/sessions/${sessionId}/evidence?limit=100`);
  if (!response.ok) throw new Error('Evidence service unavailable');
  return response.json();
}

export async function concludeSession(sessionId) {
  const response = await fetch(`${API_BASE}/api/sessions/${sessionId}/conclude`, {method: 'POST'});
  if (!response.ok) throw new Error('Conclusion service unavailable');
  return response.json();
}

export async function submitPrediction(sessionId, prediction) {
  const response = await fetch(`${API_BASE}/api/sessions/${sessionId}/prediction`, {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({prediction})
  });
  if (!response.ok) throw new Error('Prediction service unavailable');
  return response.json();
}

export async function requestHint(sessionId) {
  const response = await fetch(`${API_BASE}/api/sessions/${sessionId}/hint`, {method: 'POST'});
  if (!response.ok) throw new Error('Hint service unavailable');
  return response.json();
}

export async function restartSession(sessionId) {
  const response = await fetch(`${API_BASE}/api/sessions/${sessionId}/restart`, {method: 'POST'});
  if (!response.ok) throw new Error('Restart service unavailable');
  return response.json();
}

export async function askGenie(caseId, conversationId, question) {
  const response = await fetch(`${API_BASE}/api/genie/ask`, {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({case_id: caseId, conversation_id: conversationId || null, question})
  });
  if (!response.ok) throw new Error('Genie console unavailable');
  return response.json();
}
