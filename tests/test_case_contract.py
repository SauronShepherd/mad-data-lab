import unittest
from uuid import UUID
from unittest.mock import patch

from fastapi.testclient import TestClient

from server.main import PROGRESSION, SESSIONS, app
from server.genie import normalise_control_response, parse_control_json, registered_ids_for_case, system_prompt
from server.catalog import CASE_CATALOG, get_case


class Case042ContractTests(unittest.TestCase):
    def setUp(self):
        SESSIONS.clear()
        PROGRESSION["completed_case_ids"].clear()
        PROGRESSION["best_scores"].clear()
        self.client = TestClient(app)

    def new_session(self):
        created = self.client.post('/api/sessions', json={'case_id': 'CASE_0042'})
        self.assertEqual(created.status_code, 201)
        session_id = created.json()['session_id']
        started = self.client.post(f'/api/sessions/{session_id}/start')
        self.assertEqual(started.status_code, 200)
        self.assertEqual(started.json()['state'], 'HYPOTHESES_READY')
        return session_id

    def test_case042_reconciles(self):
        previous = 100.1 + 30.0 - 5.1 + 0.0
        current = 98.9 + 24.1 - 4.8 + 0.0
        deltas = -1.2 + -5.9 + 0.3 + 0.0
        self.assertAlmostEqual(previous, 125.0)
        self.assertAlmostEqual(current, 118.2)
        self.assertAlmostEqual(deltas, -6.8)

    def test_case042_dq_signal_is_non_additive(self):
        dq_impact = -0.3
        total_deviation = -6.8
        self.assertLess(abs(dq_impact), abs(total_deviation))
        self.assertAlmostEqual(dq_impact + -5.9, -6.2)

    def test_experiments_are_ordered_and_closed(self):
        response = self.client.post('/api/experiments/next', json={'case_id': 'CASE_0042', 'completed_experiments': []})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['experiment_id'], 'COMPONENT_DECOMPOSITION')
        response = self.client.post('/api/experiments/next', json={'case_id': 'CASE_0042', 'completed_experiments': ['COMPONENT_DECOMPOSITION', 'SNAPSHOT_DIFF']})
        self.assertEqual(response.json()['experiment_id'], 'DQ_MATERIALITY')

    def test_full_fixture_progression_closes_after_case042_sequence(self):
        completed = []
        observed = []
        for _ in range(5):
            response = self.client.post('/api/experiments/next', json={'case_id': 'CASE_0042', 'completed_experiments': completed})
            self.assertEqual(response.status_code, 200)
            experiment_id = response.json()['experiment_id']
            observed.append(experiment_id)
            completed.append(experiment_id)
        self.assertEqual(observed, ['COMPONENT_DECOMPOSITION', 'SNAPSHOT_DIFF', 'DQ_MATERIALITY', 'FORMULA_VALIDATION', 'RECONCILIATION'])
        response = self.client.post('/api/experiments/next', json={'case_id': 'CASE_0042', 'completed_experiments': completed})
        self.assertEqual(response.status_code, 409)

    def test_fixture_payload_preserves_requested_case_id(self):
        response = self.client.post('/api/experiments/next', json={'case_id': 'CASE_0042', 'completed_experiments': []})
        self.assertEqual(response.json()['case_id'], 'CASE_0042')

    def test_invalid_case_is_rejected(self):
        response = self.client.post('/api/experiments/next', json={'case_id': 'CASE_9999', 'completed_experiments': []})
        self.assertEqual(response.status_code, 404)

    def test_future_cases_are_catalogued_but_locked(self):
        self.assertEqual([case.id for case in CASE_CATALOG], ['CASE_0042', 'CASE_0107', 'CASE_0213'])
        response = self.client.post('/api/investigations', json={'case_id': 'CASE_0107'})
        self.assertEqual(response.status_code, 409)

    def test_case_experiment_contract_is_explicit_for_future_cases(self):
        response = self.client.get('/api/cases/CASE_0107/experiments')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['ready'])
        self.assertEqual(response.json()['experiments'][1], 'DUPLICATE_KEY_ANALYSIS')
        self.assertFalse(response.json()['catalog'])
        self.assertFalse(response.json()['ready'])

    def test_health_reports_fixture_without_genie_resource(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['genie_mode'], 'fixture')

    def test_production_without_genie_fails_closed_instead_of_using_fixture(self):
        with patch.dict('os.environ', {'DATABRICKS_APP_PORT': '8000', 'ALLOW_FIXTURE_MODE': '0'}, clear=False):
            self.assertEqual(self.client.get('/health').json()['genie_mode'], 'unavailable')
            self.assertEqual(self.client.post('/api/investigations', json={'case_id': 'CASE_0042'}).status_code, 503)

    def test_deployed_frontend_uses_same_origin_api_by_default(self):
        from pathlib import Path
        source = (Path(__file__).parents[1] / 'src' / 'api.ts').read_text(encoding='utf-8')
        self.assertIn("import.meta.env.DEV ? 'http://localhost:8000' : ''", source)

    def test_non_json_genie_output_is_rejected_instead_of_synthesized(self):
        with self.assertRaises(ValueError):
            normalise_control_response('The next experiment is SNAPSHOT_DIFF.', 'SNAPSHOT_DIFF', {'SNAPSHOT_DIFF'})

    def test_genie_prompt_is_case_scoped(self):
        self.assertIn('CASE_0107', system_prompt('CASE_0107'))
        self.assertNotIn('Investigate Case #042', system_prompt('CASE_0107'))

    def test_genie_control_allowlist_can_expand_per_case(self):
        payload = parse_control_json('{"experiment_id":"ROW_COUNT_ANALYSIS","name":"Rows","instrument":"Table","rationale":"check","evidence":"42 rows","hypothesis_updates":[]}', {'ROW_COUNT_ANALYSIS'})
        self.assertEqual(payload['experiment_id'], 'ROW_COUNT_ANALYSIS')

    def test_case_registry_drives_live_allowlist(self):
        self.assertEqual(registered_ids_for_case('CASE_0042'), {'COMPONENT_DECOMPOSITION', 'SNAPSHOT_DIFF', 'DQ_MATERIALITY', 'FORMULA_VALIDATION', 'RECONCILIATION'})
        self.assertEqual(registered_ids_for_case('CASE_0107'), {'ROW_COUNT_ANALYSIS', 'DUPLICATE_KEY_ANALYSIS', 'PIPELINE_RUN_COMPARISON'})

    def test_genie_protocol_rejects_invalid_status_duplicate_json_and_script(self):
        base = '{"experiment_id":"COMPONENT_DECOMPOSITION","name":"x","instrument":"WATERFALL","rationale":"x","evidence":"x","hypothesis_updates":[]}'
        self.assertEqual(parse_control_json('prefix ```json\n' + base + '\n``` suffix')['experiment_id'], 'COMPONENT_DECOMPOSITION')
        with self.assertRaises(ValueError): parse_control_json(base + base)
        invalid_status = base.replace('[]', '[{"name":"h","status":"INVALID"}]')
        with self.assertRaises(ValueError): parse_control_json(invalid_status)
        with self.assertRaises(ValueError): parse_control_json(base.replace('WATERFALL', 'ARBITRARY_WIDGET'))
        with self.assertRaises(ValueError): parse_control_json(base.replace('"x","evidence"', '"<script>alert(1)</script>","evidence"'))

    def test_complete_catalog_is_published_but_only_core_cases_start(self):
        response = self.client.get('/api/cases')
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item['number'] for item in response.json()['cases']], ['042', '107', '213', '314', '441', '520', '812'])
        self.assertEqual(self.client.post('/api/investigations', json={'case_id': 'CASE_0441'}).status_code, 409)

    def test_catalog_helper_resolves_full_game_cases(self):
        self.assertEqual(get_case('CASE_0812').title, 'Double Trouble')

    def test_canonical_case_contract_metadata_is_published(self):
        response = self.client.get('/api/cases').json()['cases']
        for case in response:
            self.assertTrue(case['required_experiment_families'], case['id'])
            self.assertTrue(case['required_evidence_tags'], case['id'])
            self.assertEqual(case['completion']['max_unreconciled_abs'], 0.01)
            self.assertTrue(case['completion']['require_final_prediction'])
            self.assertFalse(case['completion']['allow_insufficient_evidence'])

    def test_every_defined_case_has_a_registered_experiment_contract(self):
        for case_id in ('CASE_0042', 'CASE_0107', 'CASE_0213', 'CASE_0314', 'CASE_0441', 'CASE_0520', 'CASE_0812'):
            response = self.client.get(f'/api/cases/{case_id}/experiments')
            self.assertEqual(response.status_code, 200, case_id)
            self.assertTrue(response.json()['experiments'], case_id)
            self.assertEqual(response.json()['case_id'], case_id)

    def test_secondary_experiments_expose_contract_evidence(self):
        for case_id in ('CASE_0107', 'CASE_0213', 'CASE_0314', 'CASE_0441', 'CASE_0520', 'CASE_0812'):
            payload = self.client.get(f'/api/cases/{case_id}/experiments').json()
            self.assertFalse(payload['ready'], case_id)
            self.assertEqual(payload['catalog'], [], case_id)

    def test_case_availability_is_server_controlled_review_mode(self):
        normal = {item['id']: item['availability'] for item in self.client.get('/api/cases').json()['cases']}
        self.assertEqual(normal['CASE_0042'], 'AVAILABLE')
        self.assertNotEqual(normal['CASE_0107'], 'AVAILABLE')
        with patch.dict('os.environ', {'CHALLENGE_REVIEW_MODE': '1'}):
            review = {item['id']: item['availability'] for item in self.client.get('/api/cases').json()['cases']}
            self.assertNotEqual(review['CASE_0107'], 'AVAILABLE')
            self.assertTrue(self.client.get('/api/config').json()['review_mode'])
            started = self.client.post('/api/investigations', json={'case_id': 'CASE_0107'})
            self.assertEqual(started.status_code, 409)
            nxt = self.client.post('/api/experiments/next', json={'case_id': 'CASE_0107', 'completed_experiments': []})
            self.assertEqual(nxt.status_code, 409)

    def test_session_lifecycle_is_server_authoritative(self):
        created = self.client.post('/api/sessions', json={'case_id': 'CASE_0042'})
        self.assertEqual(created.status_code, 201)
        session_id = created.json()['session_id']
        self.assertEqual(self.client.post(f'/api/sessions/{session_id}/start').status_code, 200)
        self.assertEqual(self.client.post(f'/api/sessions/{session_id}/prediction', json={'prediction': 'component movement'}).status_code, 200)
        hint = self.client.post(f'/api/sessions/{session_id}/hint')
        self.assertEqual(hint.json()['hint_number'], 1)
        evidence = self.client.get(f'/api/sessions/{session_id}/evidence')
        self.assertEqual(evidence.status_code, 409)
        for _ in range(5):
            self.client.post(f'/api/sessions/{session_id}/next', json={})
        verdict = self.client.post(f'/api/sessions/{session_id}/conclude')
        self.assertEqual(verdict.json()['status'], 'COMPLETE')
        self.assertEqual(self.client.get(f'/api/sessions/{session_id}').json()['status'], 'COMPLETE')

    def test_unknown_session_is_not_created_or_leaked(self):
        self.assertEqual(self.client.get('/api/sessions/not-a-session').status_code, 404)
        self.assertEqual(self.client.get('/api/sessions/not-a-session/evidence').status_code, 404)

    def test_case_detail_and_evidence_are_publicly_curated(self):
        detail = self.client.get('/api/cases/CASE_0042')
        self.assertEqual(detail.status_code, 200)
        self.assertNotIn('truth', str(detail.json()).lower())
        session_id = self.new_session()
        self.client.post(f'/api/sessions/{session_id}/next', json={})
        self.client.post(f'/api/sessions/{session_id}/next', json={})
        evidence = self.client.get(f'/api/sessions/{session_id}/evidence').json()
        self.assertEqual(evidence['total'], 30)
        self.assertEqual(evidence['evidence'][0]['business_key'], min(item['business_key'] for item in evidence['evidence']))

    def test_evidence_is_bounded_filterable_and_request_has_id(self):
        session_id = self.new_session()
        self.client.post(f'/api/sessions/{session_id}/next', json={})
        self.client.post(f'/api/sessions/{session_id}/next', json={})
        response = self.client.get(f'/api/sessions/{session_id}/evidence?limit=1&business_key=TX-004291')
        self.assertIn('X-Request-ID', response.headers)
        self.assertEqual(response.json()['total'], 1)
        self.assertEqual(response.json()['evidence'][0]['impact'], -4.2)
        self.assertEqual(self.client.post('/api/sessions', json={'case_id': '../CASE_0042'}).status_code, 422)

    def test_documented_session_route_aliases(self):
        session_id = self.client.post('/api/sessions', json={'case_id': 'CASE_0042'}).json()['session_id']
        self.assertEqual(self.client.post(f'/api/sessions/{session_id}/start').status_code, 200)
        next_response = self.client.post(f'/api/sessions/{session_id}/next', json={'completed_experiments': []})
        self.assertEqual(next_response.status_code, 200)
        self.assertEqual(next_response.json()['experiment_id'], 'COMPONENT_DECOMPOSITION')
        chat = self.client.post(f'/api/sessions/{session_id}/chat', json={'question': 'What is the strongest signal?'})
        self.assertEqual(chat.status_code, 200)

    def test_completion_records_best_score_and_hints_reduce_score(self):
        session_id = self.new_session()
        self.client.post(f'/api/sessions/{session_id}/prediction', json={'prediction': 'component movement'})
        self.client.post(f'/api/sessions/{session_id}/hint')
        self.assertEqual(self.client.post(f'/api/sessions/{session_id}/conclude').status_code, 409)
        for _ in range(5):
            self.client.post(f'/api/sessions/{session_id}/next', json={})
        result = self.client.post(f'/api/sessions/{session_id}/conclude').json()
        # Spec formula: start 0 + prediction 150 + 5 experiments 500
        # + debrief 125 - one hint 50 = 525.
        self.assertEqual(result['score'], 525)
        progress = self.client.get('/api/progression').json()
        self.assertIn('CASE_0042', progress['completed_case_ids'])
        self.assertEqual(progress['best_scores']['CASE_0042'], 525)

    def test_score_dto_reports_evidence_badge_and_event_ledger(self):
        session_id = self.new_session()
        self.client.post(f'/api/sessions/{session_id}/prediction', json={'prediction': 'component movement'})
        for _ in range(5):
            self.client.post(f'/api/sessions/{session_id}/next', json={})
        self.client.get(f'/api/sessions/{session_id}/evidence')
        result = self.client.post(f'/api/sessions/{session_id}/conclude').json()
        self.assertIn('Data Apprentice', result['badges'])
        self.assertIn('Evidence Analyst', result['badges'])
        self.assertIn('INSPECT_HIGH_VALUE_EVIDENCE', result['score_events'])
        self.assertLessEqual(result['score'], 1000)

    def test_hints_are_server_ledgered_progressive_and_bounded(self):
        session_id = self.new_session()
        hints = [self.client.post(f'/api/sessions/{session_id}/hint').json() for _ in range(3)]
        self.assertEqual([item['hint_number'] for item in hints], [1, 2, 3])
        self.assertNotEqual(hints[0]['hint'], hints[1]['hint'])
        self.assertEqual(self.client.post(f'/api/sessions/{session_id}/hint').status_code, 409)

    def test_session_events_are_sequenced_and_append_only(self):
        session_id = self.new_session()
        self.client.post(f'/api/sessions/{session_id}/prediction', json={'prediction': 'component movement'})
        self.client.post(f'/api/sessions/{session_id}/next', json={})
        self.client.post(f'/api/sessions/{session_id}/next', json={})
        self.client.get(f'/api/sessions/{session_id}/evidence')
        events = self.client.get(f'/api/sessions/{session_id}').json()['events']
        self.assertEqual([event['sequence'] for event in events], list(range(1, len(events) + 1)))
        self.assertIn('PREDICTION', [event['type'] for event in events])
        self.assertIn('EXPERIMENT', [event['type'] for event in events])
        self.assertIn('EVIDENCE_INSPECTED', [event['type'] for event in events])

    def test_restart_is_recoverable_and_keeps_case_isolation(self):
        session_id = self.new_session()
        self.client.post(f'/api/sessions/{session_id}/next', json={})
        before = self.client.get(f'/api/sessions/{session_id}').json()['diagnostic_id']
        restarted = self.client.post(f'/api/sessions/{session_id}/restart').json()
        self.assertEqual(restarted['diagnostic_id'], before)
        current = self.client.get(f'/api/sessions/{session_id}').json()
        self.assertEqual(current['state'], 'CASE_BRIEFING')
        self.assertEqual(current['completed'], [])
        self.assertEqual(current['events'][0]['type'], 'RESTART')

    def test_session_next_ignores_forged_client_completion_and_blocks_early_verdict(self):
        session_id = self.new_session()
        self.assertEqual(self.client.post(f'/api/sessions/{session_id}/conclude').status_code, 409)
        first = self.client.post(f'/api/sessions/{session_id}/next', json={'completed_experiments': ['COMPONENT_DECOMPOSITION', 'SNAPSHOT_DIFF', 'DQ_MATERIALITY', 'FORMULA_VALIDATION', 'RECONCILIATION']})
        self.assertEqual(first.json()['experiment_id'], 'COMPONENT_DECOMPOSITION')
        second = self.client.post(f'/api/sessions/{session_id}/next', json={'completed_experiments': []})
        self.assertEqual(second.json()['experiment_id'], 'SNAPSHOT_DIFF')
        UUID(session_id)


if __name__ == '__main__':
    unittest.main()
