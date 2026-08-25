SELECT * FROM {{CURATED}}.snapshot_evidence WHERE case_id = ? ORDER BY ABS(impact) DESC, business_key LIMIT ?
