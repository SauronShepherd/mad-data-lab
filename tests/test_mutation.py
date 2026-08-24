import unittest

from server.domain import generate_case
from server.mutation import MutationOperator, mutate_records


class MutationTests(unittest.TestCase):
    def test_mutations_are_deterministic_and_preserve_null_semantics(self):
        source = generate_case().records
        for operator in MutationOperator:
            a = mutate_records(source, operator, 42)
            self.assertEqual(a, mutate_records(source, operator, 42))
            for item in a:
                if item.change_type == "ADDED": self.assertIsNone(item.old_value)
                if item.change_type == "REMOVED": self.assertIsNone(item.new_value)

    def test_structural_operators_have_expected_effect(self):
        source = generate_case().records
        self.assertLess(len(mutate_records(source, MutationOperator.MISSING_ROWS, 42)), len(source))
        self.assertGreater(len(mutate_records(source, MutationOperator.NEW_ROWS, 42)), len(source))
        self.assertGreater(len(mutate_records(source, MutationOperator.DUPLICATE_KEYS, 42)), len(source))


if __name__ == "__main__": unittest.main()
