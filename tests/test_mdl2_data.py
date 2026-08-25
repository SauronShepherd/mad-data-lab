import json
import unittest
from pathlib import Path
from decimal import Decimal
from data.generation import generate_case, FORMULA_HASH
from data.generation.generator import PHASES
from data.generation.mutations import OPERATORS, apply_operator
from data.generation.canonical import canonical_hash

class Mdl2DataTests(unittest.TestCase):
    def test_golden_values_and_hash_are_deterministic(self):
        a,b=generate_case(),generate_case(seed=42)
        self.assertEqual(a.canonical,b.canonical); self.assertEqual(a.content_hash,b.content_hash)
        self.assertEqual(a.public['expected_value'],'125.00'); self.assertEqual(a.public['observed_value'],'118.20')
        self.assertEqual(a.public['deviation'],'-6.80'); self.assertEqual(a.public['formula_hash'],FORMULA_HASH)
    def test_exact_snapshot_plan(self):
        rows=generate_case().public['snapshot_evidence']
        self.assertEqual([(kind, len([r for r in rows if r['change_type']==kind]), sum(Decimal(r['impact']) for r in rows if r['change_type']==kind)) for kind in ('MODIFIED','REMOVED','ADDED')], [('MODIFIED',23,Decimal('-5.20')),('REMOVED',2,Decimal('-0.80')),('ADDED',5,Decimal('0.10'))])
    def test_truth_is_not_in_public_projection(self):
        c=generate_case(); self.assertNotIn('truth_json', c.public); self.assertNotIn('private', c.canonical); self.assertEqual(c.private['primary_component'],'V2')
        bundle = json.loads((Path('data/fixtures/public/case_0042.bundle.json')).read_text(encoding='utf-8'))
        serialized = json.dumps(bundle, ensure_ascii=False).lower()
        for marker in ('truth_json', 'primary_cause', 'primary_component', 'secondary_cause', 'case_truth'):
            self.assertNotIn(marker, serialized)
    def test_release_seed_is_locked(self):
        with self.assertRaises(ValueError): generate_case(seed=43)
    def test_generator_exposes_all_required_phases(self):
        self.assertEqual(generate_case().phases, PHASES)
        self.assertEqual(len(PHASES), 21)
    def test_all_operator_ids_are_deterministic_and_pure(self):
        source=({'business_key':'K1','amount':'1.00'},)
        for operator in OPERATORS:
            result=apply_operator(operator, source)
            self.assertEqual(result.operator_id, operator)
            self.assertTrue(result.evidence['pure'])
        self.assertEqual(source, ({'business_key':'K1','amount':'1.00'},))
    def test_property_seeds_vary_without_changing_release_artifact(self):
        release=generate_case().content_hash
        generated={generate_case(seed=i, mode='property_test').public['property_seed'] for i in range(500)}
        self.assertEqual(len(generated), 500)
        signatures={generate_case(seed=i, mode='property_test').public['property_signature'] for i in range(500)}
        self.assertEqual(len(signatures), 500)
        self.assertEqual(generate_case().content_hash, release)
    def test_lineage_semantic_and_pipeline_evidence_are_public_and_resolvable(self):
        public=generate_case().public
        self.assertEqual(public['semantic_evidence'][0]['changed'], False)
        self.assertEqual([x['rows_written'] for x in public['pipeline_evidence']], [42,45])
        self.assertEqual(public['value_lineage'][-1]['node_id'], 'finance_reporting_source.amount')
        self.assertEqual(public['technical_lineage'][0]['lineage_source'], 'TECHNICAL_LINEAGE_FALLBACK')
        self.assertNotIn('expected_path_json', public)

    def test_canonical_domains_and_population_hashes(self):
        c = generate_case()
        self.assertEqual(set(c.canonical), {'schema_version','case_definition','datapoint_results','calculation_trace','source_snapshots','source_records','snapshot_diff','quality_issues','semantic_evidence','pipeline_evidence','technical_lineage','curated_expected_outputs'})
        self.assertNotEqual(c.canonical['source_snapshots'][0]['population_hash'], c.canonical['source_snapshots'][1]['population_hash'])
        self.assertEqual([r['pipeline_run_id'] for r in c.canonical['pipeline_evidence']], ['RUN_0042_20260802_0900','RUN_0042_20260803_0900'])
        self.assertEqual(len([r for r in c.canonical['source_records'] if r['snapshot_id']=='SNAP_20260802_0900']), 42)
        self.assertEqual(len([r for r in c.canonical['source_records'] if r['snapshot_id']=='SNAP_20260803_0900']), 45)

    def test_canonical_hash_is_independent_of_array_insertion_order(self):
        c = generate_case()
        shuffled = json.loads(json.dumps(c.canonical))
        for key in ('source_records','snapshot_diff','source_snapshots','pipeline_evidence'):
            shuffled[key].reverse()
        self.assertEqual(canonical_hash(c.canonical), canonical_hash(shuffled))

if __name__=='__main__': unittest.main()
