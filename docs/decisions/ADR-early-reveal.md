# ADR: Early reveal

Early reveal is a separate, explicit conclusion mode. It is legal only after
the Case completion predicate is satisfied, records `EARLY_REVEAL`, applies
the one-time -150 score event, and records no final prediction. Normal
conclusion requires a submitted final prediction.
