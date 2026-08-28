# Auditoría funcional y UIX — navegación completa

Fecha: 2026-08-28  
Entorno: servidor local `127.0.0.1:8000`, fixture mode  
Cobertura: portada, tablero, briefing, cinco instrumentos, evidencia, predicción, veredicto, debrief, Settings, Help y Log.

Validación remota posterior: deployment Databricks
`01f1a2e296351598889096ebdcd711ae`, ejecutado con el perfil `mdl`, en estado
`SUCCEEDED`, `genie_mode=live`; la sesión remota completó los cinco
experimentos y terminó en `DEBRIEF` con score `1000`.

Smoke oficial posterior: `PASS` (health, catálogo, sesión, cinco experimentos,
inspección de evidencias, veredicto y debrief) usando `mdl`.

## Resultado

La navegación completa es funcional: el caso se puede abrir, iniciar, recorrer
por sus cinco experimentos, concluir y abrir el debrief. Los controles de Help,
Log y Settings también funcionan y conservan foco accesible en sus diálogos.

## Pantallas y acciones verificadas

1. Portada: CTA `OPEN CASE BOARD` visible.
2. Tablero: Case #042 visible con desviación `-€6.8M`.
3. Briefing: anomalía, Dr. Genie, mapa bloqueado y selector de hipótesis.
4. Component Decomposer: V1–V4 y reconciliación `125.0 + -6.8 = 118.2`.
5. Snapshot Reactor: 23 modificados, 2 eliminados, 5 añadidos, impacto `-€5.9M`.
6. Data Quality Scanner: señal duplicada no aditiva de `-€0.3M`.
7. Formula Validator: fórmula y hash sin cambio.
8. Reconciliation Ledger: residual `€0.0M`.
9. Inspección de evidencia: registro crítico, lineage y DQ materiality.
10. Final Prediction: selección de conclusión basada en evidencia.
11. Scientific Verdict: conclusión aceptada y reconciliada.
12. Debrief: score, badges y conceptos aprendidos.
13. Settings: reduced motion.
14. Help: manual de investigación.
15. Log: cinco experimentos completados.

## UIX frente a la especificación

PASS en los rasgos observados:

- lenguaje visual de laboratorio científico pixel-art;
- fondo oscuro con acentos neon green/cyan/yellow;
- composición de panel principal más rail de Dr. Genie;
- mapa de investigación con estados locked/completed;
- separación entre instrumento, evidencia y rationale;
- progresión guiada sin saltos de estado;
- controles de recuperación y diálogos accesibles;
- badges y debrief como cierre motivacional.

## Fallos y acciones correctivas

### UX-001 — estado de catálogo engañoso durante carga

Al abrir la portada se observó temporalmente `0 CASE READY · BADGE EARNED`
antes de que terminara la carga del catálogo. El tablero posterior sí mostró
Case #042 correctamente.

Impacto: bajo, pero puede sugerir que no hay casos disponibles si el usuario
interactúa durante la ventana de carga.

Corrección aplicada: representar explícitamente `LOADING CASES…` y ocultar el
contador hasta que `catalogLoading` sea falso. Añadir assertion E2E para que el
contador no muestre cero como estado definitivo durante la carga.

### DATA-001 — score de debrief no coincide con la ruta auditada

La sesión auditada completó los cinco experimentos, inspecciones, predicción,
veredicto y debrief, pero mostró score `850` en lugar del score perfecto
esperado por el flujo completo.

Impacto: medio; afecta a la confianza en el scoring y a la trazabilidad del
resultado, aunque no bloquea el flujo.

Solución: inspeccionar el ledger de score de la sesión, identificar qué evento
no se registró durante las inspecciones y añadir una prueba E2E que afirme el
score esperado y los eventos `HIGH_VALUE_EVIDENCE_INSPECTED`,
`REQUIRED_LINEAGE_OPENED`, `FINAL_PREDICTION_CORRECT` y `FINISH_DEBRIEF`.

### NAV-002 — `REPLAY CASE` deja un estado sin CTA ejecutable

En una reproducción desde el debrief, `REPLAY CASE` volvió al panel de
investigación mostrando todos los instrumentos como `AVAILABLE`, pero el
panel central permaneció en `START INVESTIGATION`. El DOM no expuso el CTA
`RUN GENIE’S FIRST EXPERIMENT →` ni otro control equivalente, y seleccionar
una hipótesis no produjo transición.

Impacto: alto; bloquea la repetición limpia necesaria para validar scoring,
persistencia y acciones de evidencia.

Corrección aplicada: `REPLAY CASE` elimina el identificador de sesión anterior
y reutiliza el inicializador común `start(active)`, restaurando briefing,
hipótesis, experimento y CTA inicial. Falta añadir la aserción E2E específica
que ejecute `REPLAY CASE` y avance al primer instrumento.

## Reauditoría posterior a las correcciones

Se repitió el recorrido en una sesión nueva con capturas de portada, briefing,
los cinco instrumentos, evidencia, veredicto, debrief y `REPLAY CASE`. El flujo
avanzó correctamente y `REPLAY CASE` volvió al briefing con el CTA
`START INVESTIGATION →` visible y ejecutable.

El score final de esta sesión limpia fue `1000`, con los cuatro badges
esperados. `DATA-001` no se reproduce en una sesión nueva y queda clasificado
como estado persistido/acción consumida de la primera auditoría.

## Conclusión

La UIX observada está alineada con la dirección visual definida y el flujo es
usable de extremo a extremo. No se observaron bloqueos, overflow persistente,
diálogos inaccesibles ni errores visibles del navegador. UX-001 y NAV-002 han
sido corregidos en frontend; la reauditoría también confirmó score perfecto
en sesión limpia.
