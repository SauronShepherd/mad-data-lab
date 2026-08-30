import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from fastapi.testclient import TestClient
from fastapi import HTTPException

from backend.domain.completion import REQUIRED_EVIDENCE, REQUIRED_FAMILIES, evaluate_case_completion
from backend.domain.scoring import ScoreEvent, reduce_score
from backend.private.verdict_validator import validate_case042_verdict
from server.main import CREATE_IDEMPOTENCY, app, PROGRESSION, SESSIONS


class MDL4DomainTests(unittest.TestCase):
    def test_completion_requires_five_families_and_lineage_action(self):
        incomplete = evaluate_case_completion(REQUIRED_FAMILIES[:-1], REQUIRED_EVIDENCE, [])
        self.assertFalse(incomplete.ready_for_final_prediction)
        self.assertIn("RECONCILIATION_REQUIRED", incomplete.blocking_reason_codes)
        complete = evaluate_case_completion(REQUIRED_FAMILIES, REQUIRED_EVIDENCE, ["CASE_0042:LINEAGE:V2_SOURCE_PATH"])
        self.assertTrue(complete.ready_for_final_prediction)

    def test_completion_requires_each_case042_evidence_contract(self):
        for missing in ("RECONCILIATION", "FORMULA_VERSION", "DQ_MATERIALITY"):
            evidence = [item for item in REQUIRED_EVIDENCE if item != missing]
            result = evaluate_case_completion(REQUIRED_FAMILIES, evidence, ["CASE_0042:LINEAGE:V2_SOURCE_PATH"])
            self.assertFalse(result.ready_for_final_prediction)

    def test_score_replay_caps_required_experiments_and_is_idempotent(self):
        events = [ScoreEvent("START_INVESTIGATION", "START_INVESTIGATION")]
        events += [ScoreEvent("REQUIRED_EXPERIMENT_COMPLETED", f"experiment-{i}") for i in range(5)]
        events += [ScoreEvent("REQUIRED_EXPERIMENT_COMPLETED", "experiment-0")]
        self.assertEqual(reduce_score(events), 350)

    def test_verdict_validator_rejects_formula_and_dq_primary_claims(self):
        self.assertEqual(validate_case042_verdict(formula_changed=True)[0], False)
        self.assertEqual(validate_case042_verdict(dq_primary=True)[0], False)

    def test_reconciliation_failure_uses_stable_error_and_rolls_back_conclusion(self):
        SESSIONS.clear()
        client = TestClient(app)
        sid = client.post("/api/sessions", json={"case_id": "CASE_0042"}).json()["session_id"]
        session = SESSIONS[sid]
        session.update({"completed": ["COMPONENT_DECOMPOSITION", "SNAPSHOT_DIFF", "DQ_MATERIALITY", "FORMULA_VALIDATION", "RECONCILIATION"],
                        "evidence_tags": ["COMPONENT_IMPACT", "SNAPSHOT_IMPACT", "DQ_MATERIALITY", "FORMULA_VERSION", "RECONCILIATION"],
                        "inspected_capabilities": ["CASE_0042:LINEAGE:V2_SOURCE_PATH"],
                        "final_prediction": "FINAL_CHANGED_V2_SOURCE_RECORDS"})
        with patch("server.main.validate_case042_verdict", return_value=(False, ["NONZERO_UNRECONCILED_RESIDUAL"])):
            response = client.post(f"/api/sessions/{sid}/conclude")
        assert response.status_code == 422
        assert response.json()["error"]["code"] == "RECONCILIATION_FAILED"
        assert response.json()["error"]["retryable"] is False
        assert session.get("conclusion") is None
        assert session["score"] == 0
        assert session["state"] != "CONCLUDING"

    def test_prediction_ids_are_closed_for_case042(self):
        client = TestClient(app)
        SESSIONS.clear()
        CREATE_IDEMPOTENCY.clear()
        sid = client.post("/api/sessions", json={"case_id": "CASE_0042"}).json()["session_id"]
        client.post(f"/api/sessions/{sid}/start")
        self.assertEqual(client.post(f"/api/sessions/{sid}/prediction", json={"prediction": "not-a-choice"}).status_code, 422)

    def test_score_golden_scenarios(self):
        base = [ScoreEvent("START_INVESTIGATION", "start"), ScoreEvent("INITIAL_PREDICTION_SUBMITTED", "initial"), ScoreEvent("INITIAL_PREDICTION_CORRECT", "initial-correct")]
        base += [ScoreEvent("REQUIRED_EXPERIMENT_COMPLETED", f"exp-{i}") for i in range(3)]
        base += [ScoreEvent("HIGH_VALUE_EVIDENCE_INSPECTED", "high"), ScoreEvent("REQUIRED_LINEAGE_OPENED", "lineage"), ScoreEvent("FINAL_PREDICTION_CORRECT", "final"), ScoreEvent("FINISH_DEBRIEF", "debrief")]
        self.assertEqual(reduce_score(base), 1000)
        self.assertEqual(reduce_score(base[:-1] + [ScoreEvent("HINT_REVEALED", "hint-1"), base[-1]]), 950)
        self.assertEqual(reduce_score(base[:-2] + [ScoreEvent("EARLY_REVEAL", "early"), base[-1]]), 650)

    def test_all_locked_score_golden_scenarios(self):
        common = [
            ScoreEvent("START_INVESTIGATION", "start"),
            ScoreEvent("INITIAL_PREDICTION_SUBMITTED", "initial"),
            ScoreEvent("INITIAL_PREDICTION_CORRECT", "initial-correct"),
            *(ScoreEvent("REQUIRED_EXPERIMENT_COMPLETED", f"exp-{i}") for i in range(3)),
            ScoreEvent("HIGH_VALUE_EVIDENCE_INSPECTED", "high"),
            ScoreEvent("REQUIRED_LINEAGE_OPENED", "lineage"),
            ScoreEvent("FINAL_PREDICTION_CORRECT", "final"),
            ScoreEvent("FINISH_DEBRIEF", "debrief"),
        ]
        self.assertEqual(reduce_score(common), 1000)  # PERFECT
        self.assertEqual(reduce_score([e for e in common if e.eligibility_key != "initial-correct"]), 900)  # WRONG_INITIAL_CORRECT_FINAL
        self.assertEqual(reduce_score(common + [ScoreEvent("HINT_REVEALED", "hint-1")]), 950)  # ONE_HINT
        self.assertEqual(reduce_score(common + [ScoreEvent("HINT_REVEALED", f"hint-{i}") for i in range(1, 4)]), 850)  # ALL_THREE_HINTS
        self.assertEqual(reduce_score([e for e in common if e.eligibility_key != "high"]), 900)  # SKIP_HIGH_VALUE_RECORD
        early = [e for e in common if e.score_type not in {"FINAL_PREDICTION_CORRECT", "FINISH_DEBRIEF"}]
        self.assertEqual(reduce_score(early + [ScoreEvent("EARLY_REVEAL", "early"), ScoreEvent("FINISH_DEBRIEF", "debrief")]), 650)  # EARLY_REVEAL_CORRECT_INITIAL
        wrong_early = [e for e in early if e.eligibility_key != "initial-correct"]
        self.assertEqual(reduce_score(wrong_early + [ScoreEvent("EARLY_REVEAL", "early"), ScoreEvent("FINISH_DEBRIEF", "debrief")]), 550)  # EARLY_REVEAL_WRONG_INITIAL


class MDL4FlowTests(unittest.TestCase):
    def setUp(self):
        SESSIONS.clear()
        CREATE_IDEMPOTENCY.clear()
        PROGRESSION["completed_case_ids"].clear()
        PROGRESSION["best_scores"].clear()
        self.client = TestClient(app)

    def test_fake_case042_reaches_verdict_then_debrief(self):
        created = self.client.post("/api/sessions", json={"case_id": "CASE_0042"})
        self.assertEqual(created.status_code, 201)
        sid = created.json()["session_id"]
        self.assertNotIn("score", created.json())
        self.assertEqual(self.client.post(f"/api/sessions/{sid}/start").status_code, 200)
        self.client.post(f"/api/sessions/{sid}/prediction", json={"prediction": "PRED_SOURCE_VALUES_CHANGED"})
        for _ in range(5):
            self.assertEqual(self.client.post(f"/api/sessions/{sid}/next", json={}).status_code, 200)
        final_stage = self.client.post(f"/api/sessions/{sid}/next", json={})
        self.assertEqual(final_stage.json()["phase"], "PLAYER_PREDICTION_FINAL")
        inspect = self.client.post(f"/api/sessions/{sid}/evidence/inspect", json={"capability": "CASE_0042:LINEAGE:V2_SOURCE_PATH"})
        self.assertEqual(inspect.status_code, 200)
        inspect_replay = self.client.post(f"/api/sessions/{sid}/evidence/inspect", headers={"Idempotency-Key": "lineage-once"}, json={"capability": "CASE_0042:RECORD:TX-004291"})
        inspect_replay_again = self.client.post(f"/api/sessions/{sid}/evidence/inspect", headers={"Idempotency-Key": "lineage-once"}, json={"capability": "CASE_0042:RECORD:TX-004291"})
        self.assertEqual(inspect_replay.json(), inspect_replay_again.json())
        self.client.post(f"/api/sessions/{sid}/prediction", json={"final": True, "prediction": "FINAL_CHANGED_V2_SOURCE_RECORDS"})
        verdict = self.client.post(f"/api/sessions/{sid}/conclude", json={})
        self.assertEqual(verdict.status_code, 200)
        self.assertEqual(verdict.json()["state"], "CONCLUDING")
        self.assertIn("score", self.client.get(f"/api/sessions/{sid}").json())
        debrief = self.client.post(f"/api/sessions/{sid}/debrief", json={})
        self.assertEqual(debrief.status_code, 200)
        self.assertEqual(debrief.json()["state"], "DEBRIEF")
        self.assertIn("score", debrief.json())
        score_events = list(SESSIONS[sid]["score_events"])
        second_debrief = self.client.post(f"/api/sessions/{sid}/debrief", json={})
        self.assertEqual(second_debrief.status_code, 200)
        self.assertEqual(second_debrief.json()["score"], debrief.json()["score"])
        self.assertEqual(SESSIONS[sid]["score_events"], score_events)

    def test_live_duplicate_experiment_cannot_be_committed(self):
        sid = self.client.post("/api/sessions", json={"case_id": "CASE_0042"}).json()["session_id"]
        self.client.post(f"/api/sessions/{sid}/start")
        from unittest.mock import patch
        with patch("server.main.next_experiment", return_value={"experiment_id": "SNAPSHOT_DIFF", "source": "genie"}):
            first = self.client.post(f"/api/sessions/{sid}/next", json={})
            self.assertEqual(first.status_code, 200)
            second = self.client.post(f"/api/sessions/{sid}/next", json={})
        self.assertEqual(second.status_code, 200)
        self.assertEqual(first.json()["experiment_id"], "COMPONENT_DECOMPOSITION")
        self.assertEqual(second.json()["experiment_id"], "SNAPSHOT_DIFF")
        self.assertEqual(len(SESSIONS[sid]["completed"]), 2)

    def test_session_projection_never_exposes_private_truth_or_score_ledger(self):
        sid = self.client.post("/api/sessions", json={"case_id": "CASE_0042"}).json()["session_id"]
        projection = self.client.get(f"/api/sessions/{sid}").json()
        self.assertNotIn("private_truth", projection)
        self.assertNotIn("score_ledger", projection)
        self.assertNotIn("score", projection)

    def test_final_prediction_cannot_bypass_analytical_completion(self):
        sid = self.client.post("/api/sessions", json={"case_id": "CASE_0042"}).json()["session_id"]
        self.client.post(f"/api/sessions/{sid}/start")
        response = self.client.post(f"/api/sessions/{sid}/prediction", json={"final": True, "prediction": "FINAL_CHANGED_V2_SOURCE_RECORDS"})
        self.assertEqual(response.status_code, 409)
        self.assertEqual(SESSIONS[sid].get("final_prediction"), None)

    def test_session_creation_replays_same_idempotency_key(self):
        headers = {"Idempotency-Key": "create-once"}
        first = self.client.post("/api/sessions", headers=headers, json={"case_id": "CASE_0042"})
        replay = self.client.post("/api/sessions", headers=headers, json={"case_id": "CASE_0042"})
        self.assertEqual(first.status_code, 201)
        self.assertEqual(replay.status_code, 201)
        self.assertEqual(replay.json(), first.json())
        self.assertEqual(len(SESSIONS), 1)

    def test_cross_case_case042_evidence_is_forbidden(self):
        created = self.client.post("/api/sessions", json={"case_id": "CASE_001"})
        if created.status_code != 201:
            self.skipTest("CASE_001 is not enabled in the current catalog")
        sid = created.json()["session_id"]
        response = self.client.post(f"/api/sessions/{sid}/evidence/inspect", json={"capability": "CASE_0042:RECORD:TX-004291"})
        self.assertEqual(response.status_code, 403)

    def test_early_reveal_is_only_legal_after_analysis_and_applies_penalty(self):
        sid = self.client.post("/api/sessions", json={"case_id":"CASE_0042"}).json()["session_id"]
        self.client.post(f"/api/sessions/{sid}/start")
        self.assertEqual(self.client.post(f"/api/sessions/{sid}/conclude", json={"mode":"EARLY_REVEAL"}).status_code, 409)
        for _ in range(5): self.client.post(f"/api/sessions/{sid}/next", json={})
        self.client.post(f"/api/sessions/{sid}/evidence/inspect", json={"capability":"CASE_0042:LINEAGE:V2_SOURCE_PATH"})
        verdict = self.client.post(f"/api/sessions/{sid}/conclude", json={"mode":"EARLY_REVEAL"})
        self.assertEqual(verdict.status_code, 200)
        self.assertEqual(SESSIONS[sid]["final_prediction"], "SKIPPED_BY_EARLY_REVEAL")
        self.assertIn("EARLY_REVEAL", SESSIONS[sid]["score_events"])

    def test_revision_conflict_and_idempotent_prediction_replay(self):
        sid = self.client.post("/api/sessions", json={"case_id":"CASE_0042"}).json()["session_id"]
        self.client.post(f"/api/sessions/{sid}/start")
        before = self.client.get(f"/api/sessions/{sid}").json()["state_revision"]
        stale = self.client.post(f"/api/sessions/{sid}/prediction", headers={"Idempotency-Key":"p-1"}, json={"prediction":"PRED_SOURCE_VALUES_CHANGED", "expected_state_revision": before - 1})
        self.assertEqual(stale.status_code, 409)
        first = self.client.post(f"/api/sessions/{sid}/prediction", headers={"Idempotency-Key":"p-1"}, json={"prediction":"PRED_SOURCE_VALUES_CHANGED", "expected_state_revision": before})
        replay = self.client.post(f"/api/sessions/{sid}/prediction", headers={"Idempotency-Key":"p-1"}, json={"prediction":"PRED_SOURCE_VALUES_CHANGED", "expected_state_revision": before})
        self.assertEqual(first.status_code, 200)
        self.assertEqual(replay.json(), first.json())
        self.assertEqual(len([e for e in SESSIONS[sid]["events"] if e["type"] == "INITIAL_PREDICTION_SUBMITTED"]), 1)

    def test_live_genie_failure_uses_safe_registered_recovery(self):
        sid = self.client.post("/api/sessions", json={"case_id": "CASE_0042"}).json()["session_id"]
        self.client.post(f"/api/sessions/{sid}/start")
        SESSIONS[sid]["conversation_id"] = "live-conversation"

        class FailedLiveGenie:
            enabled = True

            def next(self, *_args, **_kwargs):
                raise HTTPException(status_code=503, detail="unavailable")

        with patch("server.main.genie", FailedLiveGenie()):
            response = self.client.post(f"/api/sessions/{sid}/next", json={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["source"], "genie-recovery-continuation")
        self.assertEqual(SESSIONS[sid]["completed"], ["COMPONENT_DECOMPOSITION"])

    def test_expired_session_is_not_reconstructed_and_restart_uses_new_id(self):
        sid = self.client.post("/api/sessions", json={"case_id": "CASE_0042"}).json()["session_id"]
        SESSIONS[sid]["last_activity"] = (datetime.now(timezone.utc) - timedelta(hours=3)).isoformat()
        expired = self.client.get(f"/api/sessions/{sid}")
        self.assertEqual(expired.status_code, 410)
        self.assertEqual(expired.json()["detail"]["code"], "SESSION_EXPIRED")
        restarted = self.client.post(f"/api/sessions/{sid}/restart")
        self.assertEqual(restarted.status_code, 200)
        self.assertNotEqual(restarted.json()["session_id"], sid)
        self.assertEqual(restarted.json()["state"], "CASE_BRIEFING")
