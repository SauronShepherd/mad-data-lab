from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Experiment:
    id: str
    name: str
    instrument: str
    rationale: str
    evidence: str
    updates: tuple[tuple[str, str], ...]


EXPERIMENTS = (
    Experiment(
        "EXP-01",
        "Deviation Decomposer",
        "Waterfall instrument",
        "V2 carries most of the unexplained movement, so I am splitting the metric into its components.",
        "The V2 component explains €5.9M of the €6.8M deviation — 87% of the anomaly.",
        (("Promo effect?", "POSSIBLE"), ("Data bug?", "POSSIBLE"), ("Pricing change?", "SUPPORTED"), ("Seasonal factor?", "SUPPORTED")),
    ),
    Experiment(
        "EXP-02",
        "Snapshot Reactor",
        "Snapshot comparison",
        "The largest signal is in V2. I am comparing the previous and current snapshots to find the changed records.",
        "30 V2 records changed: 23 modified, 2 removed, 5 added. Net impact: -€5.9M.",
        (("Promo effect?", "SUPPORTED"), ("Data bug?", "SUPPORTED"), ("Pricing change?", "SUPPORTED"), ("Seasonal factor?", "RULED_OUT")),
    ),
    Experiment(
        "EXP-03",
        "Evidence Microscope",
        "Record-level evidence",
        "One representative source record can reconcile the aggregate result without guessing at causality.",
        "TX-004291 moved from €4.2M to €0.0M, contributing -€4.2M to the V2 change.",
        (("Promo effect?", "RULED_OUT"), ("Data bug?", "SUPPORTED"), ("Pricing change?", "RULED_OUT"), ("Seasonal factor?", "RULED_OUT")),
    ),
)

EXPERIMENTS_BY_CASE = {
    "CASE_0042": EXPERIMENTS,
}

PLANNED_EXPERIMENTS_BY_CASE = {
    "CASE_0107": (
        Experiment("ROW_COUNT_ANALYSIS", "Row Count Analyzer", "Population counter", "Check whether the metric population changed before inspecting duplicates.", "ROW_COUNT_DELTA: 12,481 -> 12,736 (+255 rows).", ()),
        Experiment("DUPLICATE_KEY_ANALYSIS", "Duplicate Key Scanner", "Key collision microscope", "Test whether repeated business keys inflate the metric.", "DUPLICATE_IMPACT: duplicate impact reconciles to +1.8M EUR.", ()),
        Experiment("PIPELINE_RUN_COMPARISON", "Pipeline Run Comparator", "Run timeline", "Compare pipeline executions to distinguish replay from a legitimate business change.", "PIPELINE_REPLAY: causal run replays the original and writes 255 duplicate rows.", ()),
    ),
    "CASE_0213": (
        Experiment("FILTER_VALIDATION", "Filter Validator", "Population lens", "Test whether a filter removed valid records from the recognized-revenue population.", "FILTER_HASH_CHANGE: changed=true; affected population=74.", ()),
        Experiment("RECONCILIATION", "Revenue Reconciler", "Balance scope", "Reconcile the excluded population back to the reported metric.", "EXCLUDED_POPULATION + EXCLUDED_IMPACT: 74 rows account for -6.5M EUR.", ()),
    ),
}

PLANNED_EXPERIMENTS_BY_CASE.update({
    "CASE_0314": tuple(Experiment(i, n, u, r, "Deterministic fixture evidence is available for this experiment.", ()) for i, n, u, r in (
        ("ROW_COUNT_ANALYSIS", "Row Count Analyzer", "Population counter", "Compare previous and current population counts."),
        ("MISSING_RECORD_IMPACT", "Missing Record Microscope", "Evidence table", "Measure the value of missing records."),
        ("RECONCILIATION", "Exposure Reconciler", "Balance view", "Reconcile the missing population to the deviation."),)),
    "CASE_0441": tuple(Experiment(i, n, u, r, "Deterministic fixture evidence is available for this experiment.", ()) for i, n, u, r in (
        ("DQ_MATERIALITY", "Quality Scanner", "DQ panel", "Measure the quality warning and its overlap."),
        ("RECONCILIATION", "Margin Reconciler", "Balance view", "Reconcile the primary source movement."),)),
    "CASE_0520": tuple(Experiment(i, n, u, r, "Deterministic fixture evidence is available for this experiment.", ()) for i, n, u, r in (
        ("ENTITY_COMPARISON", "Entity Comparator", "Comparison view", "Compare entity populations."),
        ("JOIN_CARDINALITY_ANALYSIS", "Cardinality Matrix", "Cardinality matrix", "Measure join multiplication."),
        ("RECONCILIATION", "Forecast Reconciler", "Balance view", "Reconcile the inflated forecast."),)),
    "CASE_0812": tuple(Experiment(i, n, u, r, "Deterministic fixture evidence is available for this experiment.", ()) for i, n, u, r in (
        ("COMPONENT_DECOMPOSITION", "Component Decomposer", "Waterfall", "Split the multi-cause deviation."),
        ("SNAPSHOT_DIFF", "Snapshot Reactor", "Snapshot comparison", "Compare changed source records."),
        ("FILTER_VALIDATION", "Filter Validator", "Population lens", "Test population selection."),
        ("RECONCILIATION", "Multi-cause Reconciler", "Balance view", "Reconcile all causes."),)),
})

# Contract-level evidence tags are intentionally present in the fixture response;
# they let the UI and tests distinguish an approved instrument from an
# unsupported narrative claim.
EVIDENCE_BY_EXPERIMENT = {
    "ROW_COUNT_ANALYSIS": "MISSING_ROW_COUNT: previous and current population counts are compared.",
    "MISSING_RECORD_IMPACT": "MISSING_IMPACT: missing records reconcile to -5.2M EUR.",
    "DQ_MATERIALITY": "DQ_IMPACT: quality warning is measured for materiality and overlap.",
    "JOIN_CARDINALITY_ANALYSIS": "JOIN_MULTIPLICITY: repeated join keys explain the inflated rows.",
    "ENTITY_COMPARISON": "ENTITY_OUTLIER: an abnormal entity population concentration is isolated.",
    "COMPONENT_DECOMPOSITION": "SOURCE_CAUSE_IMPACT: first causal component is quantified.",
    "SNAPSHOT_DIFF": "FILTER_CAUSE_IMPACT: changed snapshot population is quantified.",
}
EVIDENCE_BY_CASE_EXPERIMENT = {
    ("CASE_0107", "ROW_COUNT_ANALYSIS"): "ROW_COUNT_DELTA: 12,481 -> 12,736 (+255 rows).",
    ("CASE_0314", "ROW_COUNT_ANALYSIS"): "MISSING_ROW_COUNT: previous and current population counts are compared.",
}


def experiment_payload(experiment: Experiment, index: int, case_id: str = "CASE_0042") -> dict:
    return {
        "case_id": case_id,
        "experiment_id": experiment.id,
        "experiment_number": index + 1,
        "name": experiment.name,
        "instrument": experiment.instrument,
        "rationale": experiment.rationale,
        "evidence": EVIDENCE_BY_CASE_EXPERIMENT.get((case_id, experiment.id), EVIDENCE_BY_EXPERIMENT.get(experiment.id, experiment.evidence)),
        "hypothesis_updates": [{"name": name, "status": status} for name, status in experiment.updates],
        "source": "fixture",
    }
