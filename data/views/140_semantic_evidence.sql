SELECT *, (COALESCE(previous_hash,'') <> COALESCE(current_hash,'') OR COALESCE(previous_id,'') <> COALESCE(current_id,'')) AS changed FROM {{PUBLIC}}.semantic_change_evidence
