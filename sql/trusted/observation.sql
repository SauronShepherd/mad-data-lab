-- Keep the trusted result schema deterministic.  The curated view is built
-- from a join and SELECT * can expose duplicate case_id columns through
-- connector metadata; dict(zip(...)) would then retain the wrong value.
SELECT case_id, public_number, slug, seed, generator_version,
       case_template_version, title, hook, datapoint_id, entity_id,
       period_id, expected_value, observed_value, deviation, currency,
       scale, difficulty, release_state, sort_order, required_case_ids,
       learning_objectives, status, created_at, current_run_id,
       previous_run_id, current_formula_id, previous_formula_id,
       current_formula_hash, previous_formula_hash
FROM {{CURATED}}.case_summary
WHERE case_id = ?
