# Genie at the Core

Dr. Genie selects a currently legal, registry-controlled Experiment and Instrument from the validated protocol. The player supplies a prediction; the player does not route analytical Experiments.

The request lifecycle is: server-authoritative session state → validated Genie selection → trusted query/evidence projection → hypothesis transition → append-only event history. Unknown Experiments, instruments, filters, evidence references, and malformed protocol versions fail closed.

If live Genie is unavailable, the application exposes an explicit deterministic failure/recovery state. It does not present fixture output as a live Genie success, and private Case truth never enters the Genie or browser boundary.
