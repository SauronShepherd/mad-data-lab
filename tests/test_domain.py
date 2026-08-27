import unittest

from server.domain import CASE_SPECS, canonical_json, fixture_hash, generate_case, validate_fixture


class DeterministicCaseTests(unittest.TestCase):
    def test_case042_golden_invariants(self):
        fixture = generate_case()
        validate_fixture(fixture)
        self.assertEqual((fixture.expected, fixture.observed, fixture.deviation), (125.0, 118.2, -6.8))
        self.assertEqual(fixture_hash(fixture), "189756bae236c38b946948dcf7859eca1062b34ed40a25c2b4304f7eb8e49f25")
        self.assertEqual([(c.previous, c.current, c.delta) for c in fixture.components], [(100.1, 98.9, -1.2), (30.0, 24.1, -5.9), (5.1, 4.8, 0.3), (0.0, 0.0, 0.0)])
        self.assertEqual([r.change_type for r in fixture.records].count("MODIFIED"), 23)
        self.assertEqual([r.change_type for r in fixture.records].count("REMOVED"), 2)
        self.assertEqual([r.change_type for r in fixture.records].count("ADDED"), 5)
        self.assertAlmostEqual(sum(r.impact for r in fixture.records if r.change_type == "MODIFIED"), -5.2)
        self.assertAlmostEqual(fixture.snapshot_total, -5.9)
        self.assertEqual(next(r for r in fixture.records if r.business_key == "TX-004291").impact, -4.2)
        self.assertEqual((fixture.dq_affected_rows, fixture.dq_estimated_impact, fixture.dq_overlap), (5, -0.3, True))
        self.assertEqual(fixture.truth.primary_component, "V2")
        self.assertEqual(fixture.truth.primary_cause, "SOURCE_RECORD_CHANGE")

    def test_same_seed_is_byte_stable_and_other_seed_varies(self):
        a, b, c = generate_case(), generate_case(), generate_case(seed=43)
        self.assertEqual(canonical_json(a.curated_projection()), canonical_json(b.curated_projection()))
        self.assertNotEqual(fixture_hash(a), fixture_hash(c))
        self.assertEqual(a.generator_version, 2)

    def test_curated_projection_has_no_private_truth(self):
        projection = generate_case().curated_projection()
        self.assertNotIn("truth", projection)
        self.assertNotIn("primary_component", canonical_json(projection))

    def test_record_null_semantics(self):
        fixture = generate_case()
        for record in fixture.records:
            if record.change_type == "ADDED": self.assertIsNone(record.old_value)
            if record.change_type == "REMOVED": self.assertIsNone(record.new_value)
            if record.change_type == "MODIFIED": self.assertIsNotNone(record.old_value); self.assertIsNotNone(record.new_value)

    def test_all_seven_case_observations_and_truth_are_materialized(self):
        for case_id, spec in CASE_SPECS.items():
            fixture = generate_case(case_id, int(spec['seed']))
            validate_fixture(fixture)
            self.assertEqual((fixture.expected, fixture.observed), (spec['expected'], spec['observed']), case_id)
            self.assertEqual(fixture.deviation, round(spec['observed'] - spec['expected'], 2))
            self.assertEqual(fixture.truth.primary_cause, spec['primary_cause'])
            self.assertTrue(fixture.curated_projection()['records'], case_id)
            self.assertAlmostEqual(fixture.component_total, fixture.deviation)


if __name__ == "__main__":
    unittest.main()
