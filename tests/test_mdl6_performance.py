from scripts import performance_gate


def test_production_bundle_meets_mdl6_budgets():
    performance_gate.main()
