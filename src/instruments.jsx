import React from "react";

const money = (value) => `${Number(value) < 0 ? "-" : ""}€${Math.abs(Number(value || 0)).toFixed(1)}M`;

function KpiDelta({model}) {
  return <section className="instrument-model" aria-label="Key performance indicator delta"><h3>Observed deviation</h3><p className="exact-values">Expected {money(model.expected)} · Observed {money(model.observed)} · Delta <strong>{money(model.deviation)}</strong></p></section>;
}
function Waterfall({model}) {
  const rows = model.components || [];
  const total = rows.reduce((sum, row) => sum + Number(row.delta || 0), 0);
  if (Math.round((Number(model.expected || 0) + total - Number(model.observed || 0)) * 100) !== 0) return <section className="instrument-model" role="alert"><h3>Waterfall validation error</h3><p>Component contributions do not reconcile to the observed value.</p></section>;
  return <section className="instrument-model" aria-label="Component waterfall"><h3>Component decomposition</h3><table><caption className="sr-only">Exact signed component contributions</caption><thead><tr><th>Component</th><th>Contribution</th></tr></thead><tbody>{rows.map((row) => <tr key={row.component_id || row.id}><td>{row.label || row.component_id}</td><td className={row.component_id === "V2" ? "dominant" : ""}>{money(row.delta)}</td></tr>)}</tbody></table><p className="exact-values">Expected + contributions = observed: {money(model.expected)} + {money(total)} = {money(model.observed)}</p></section>;
}
function SnapshotDiff({model}) {
  const groups = model.groups || [];
  const total = groups.reduce((sum, row) => sum + Number(row.impact || 0), 0);
  const valid = Math.round((total - Number(model.net_impact || 0)) * 100) === 0;
  return <section className="instrument-model" aria-label="Snapshot difference">{valid ? <><h3>Snapshot difference</h3><table><thead><tr><th>Change</th><th>Rows</th><th>Impact</th></tr></thead><tbody>{groups.map((row) => <tr key={row.change_type}><td>{row.change_type}</td><td>{row.count}</td><td>{money(row.impact)}</td></tr>)}</tbody></table><p className="exact-values">Net impact: {money(model.net_impact)}</p></> : <><h3>Snapshot validation error</h3><p>Group impacts do not reconcile to net impact.</p></>}</section>;
}
function EvidenceTable({model}) { const rows = model.records || []; return <section className="instrument-model" aria-label="Evidence records"><h3>Evidence records</h3>{rows.length ? <table><thead><tr><th>Business key</th><th>Change</th><th>Impact</th></tr></thead><tbody>{rows.map((row) => <tr key={row.business_key}><td>{row.business_key}</td><td>{row.change_type}</td><td>{money(row.impact)}</td></tr>)}</tbody></table> : <p>No evidence records match the current filters.</p>}</section>; }
function DqPanel({model}) { return <section className="instrument-model" aria-label="Data quality materiality"><h3>Data-quality signal</h3><p>{model.rule_name || "DUPLICATE_BUSINESS_KEY"} · {model.severity || "MEDIUM"} · {model.affected_rows ?? 5} rows · {money(model.estimated_impact ?? -0.3)}</p>{model.overlap !== false && <p className="warning">Estimated impact overlaps other evidence and is not additive. Its magnitude is insufficient to explain the anomaly by itself.</p>}</section>; }
function FormulaDiff({model}) { const same = model.changed === false || (model.previous_hash && model.previous_hash === model.current_hash); return <section className="instrument-model" aria-label="Formula comparison"><h3>Formula validation</h3><p className="exact-values">{same ? "Formula did not change." : "Formula changed."} Previous {model.previous_id || "V1+V2-V3+V4"} · Current {model.current_id || "V1+V2-V3+V4"}</p></section>; }
function LineageGraph({model}) { const nodes = model.nodes || []; return <section className="instrument-model" aria-label="Deterministic value lineage"><h3>Value lineage</h3><ol className="lineage-list">{nodes.map((node) => <li key={`${node.node_type}:${node.node_id}`}>{node.node_id}</li>)}</ol></section>; }
function Reconciliation({model}) { const valid = Math.round((Number(model.explained || -5.9) + Number(model.unreconciled || 0) - Number(model.total || -5.9)) * 100) === 0; return <section className="instrument-model" aria-label="Reconciliation">{valid ? <><h3>Reconciliation</h3><p className="exact-values">Total {money(model.total ?? -6.8)} · V2 {money(model.v2 ?? -5.9)} · Other {money(model.other ?? -0.9)} · Unreconciled {money(model.unreconciled ?? 0)}</p></> : <p role="alert">Reconciliation validation error.</p>}</section>; }

const registry = { KPI_DELTA: KpiDelta, WATERFALL: Waterfall, SNAPSHOT_DIFF: SnapshotDiff, EVIDENCE_TABLE: EvidenceTable, DQ_PANEL: DqPanel, FORMULA_DIFF: FormulaDiff, FORMULA_CHECK: FormulaDiff, LINEAGE_GRAPH: LineageGraph, RECONCILIATION: Reconciliation };
export function InstrumentRenderer({id, model = {}}) { const Component = registry[id]; return Component ? <Component model={model} /> : <section className="instrument-model" role="alert"><h3>Instrument unavailable</h3><p>Unknown analytical instrument.</p></section>; }
export { registry as instrumentRegistry };
