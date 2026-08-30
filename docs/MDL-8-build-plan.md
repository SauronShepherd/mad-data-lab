# MAD DATA LAB — build plan de cierre y submission

Este documento es el checklist operativo de bajo nivel para pasar de la implementación actual a una submission verificable. `PASS` significa que existe evidencia ejecutable en este checkout; `PENDING_EXTERNAL` requiere una cuenta, aprobación o sistema externo.

## 1. Fundación y contrato canónico — MDL-1

- [x] Confirmar jerarquía `Case → Investigation → Experiment → Evidence → Hypothesis Update → Verdict`.
- [x] Mantener Case #042 sintético, determinista y multi-Case desde catálogo.
- [x] Mantener separación entre truth privada, repositorio público y Genie.
- [x] Ejecutar tests de dominio, contratos, modelos y trazabilidad.
- [x] Recuperar y conservar artefactos históricos de predecessor.
- [x] Archivar la fuente canónica V3 y verificar su SHA-256 contra la referencia suministrada.
- [x] CI/branch protection excluidos del alcance por decisión del propietario del proyecto.
- [x] Excluir aprobación humana de assets por decisión del propietario; conservar preflight técnico.

## 2. Datos y evidencia — MDL-2

- [x] Validar DDL, fixtures, generator determinista y hashes.
- [x] Validar grupos exactos: 23 modified, 2 removed, 5 added, 14 unchanged.
- [x] Validar DQ como evidencia no aditiva.
- [x] Validar vistas curated y query registry sin SQL arbitrario.
- [x] Validar exclusión de `CASE_TRUTH` en la superficie pública.
- [x] Actualizar digest y artefactos de contrato al runtime actual.
- [x] Verificar remotamente en Databricks profile `mdl`.
- [ ] `PENDING_EXTERNAL`: seed/rollback final sobre warehouse de producción y evidencia de despliegue.

## 3. Genie y orquestación — MDL-3

- [x] Validar registry de cinco experimentos y protocolo estricto.
- [x] Validar bounded queries, rechazo de IDs no registrados y fallback seguro.
- [x] Ejecutar benchmark/contrato local y actualizar runtime/config digests.
- [x] Mantener Genie sin acceso a truth privada.
- [ ] `PENDING_EXTERNAL`: benchmark live autenticado para el source identity final.
- [ ] `PENDING_EXTERNAL`: soak de Genie y evidencia de plataforma.

## 4. Flujo de juego y scoring — MDL-4

- [x] Validar estados server-authoritative y transiciones idempotentes.
- [x] Validar predicción inicial, experimentos, inspección, conclusión y debrief.
- [x] Validar score, badges, early reveal y replay.
- [x] Corregir navegación `OPEN CASE BOARD → OPEN CASE → briefing`.
- [x] Verificar recorrido completo Case #042 hasta verdict/debrief.
- [ ] `PENDING_EXTERNAL`: revalidar manifest histórico en el commit final desplegado.

## 5. Instruments, Evidence Explorer y UIX — MDL-5

- [x] Validar InstrumentRenderer contra modelos de evidencia registrados.
- [x] Validar navegación de evidencia, record, lineage y DQ materiality.
- [x] Validar teclado, dialogs, labels, audio y reduced motion.
- [x] Validar assets PNG y audio preflight.
- [x] Añadir rutas públicas: library, articles, groups, variants, feedback, comments, account y admin.
- [x] Añadir deep-link fallback de servidor para rutas públicas.
- [x] Añadir persistencia local de idioma/tema/feedback/comments.
- [ ] Añadir backend autenticado de comentarios y suscripción para producción real.
- [x] Excluir aprobación exact-byte humana por decisión del propietario; preflight técnico PASS.

## 6. Hardening — MDL-6

- [x] Error envelope seguro y request IDs.
- [x] Retry/circuit breaker/fallback y recuperación de sesión.
- [x] Autoplay rechazado sin bloquear gameplay.
- [x] Asset 404 sin romper controles.
- [x] Validar responsive contra overflow horizontal y controles fuera de pantalla.
- [x] Regenerar matriz de escenarios desde el script para evitar CSV desincronizado.
- [x] Ejecutar suite Python completa: 301 passed, 7 skipped.
- [x] Ejecutar suite MDL-6 browser: 11 passed.

## 7. Release candidate — MDL-7

- [x] Build y typecheck reproducibles.
- [x] Browser smoke principal y responsive ejecutables.
- [x] Artefactos históricos conservados y digests actualizados.
- [ ] Ejecutar `release_candidate.py` sobre source identity final.
- [ ] Resolver cualquier gate local que dependa de configuración externa.
- [ ] `PENDING_EXTERNAL`: deployed smoke, deployed soak y live Genie.

## 8. Submission freeze — MDL-8

- [x] Generar capturas desktop 1440×900, tablet 1024×768 y móvil 390×844.
- [x] Capturar landing, case board, briefing e investigation.
- [x] Capturar cada ruta pública en los tres viewports.
- [x] Emitir `ui-diagnostic.json` con overflow, offscreen, broken images y empty buttons.
- [x] Generar verificación remota Databricks.
- [x] Mantener informe honesto con pendientes externos.
- [ ] Capturar verdict/debrief y acciones individuales del flujo completo para el paquete final.
- [ ] Sustituir placeholders del Community Article por capturas/enlaces finales.
- [ ] Generar y revisar vídeo demo de 2:44 según timeline MDL-8.
- [ ] Validar landing URL y app URL públicas.
- [x] Excluir aprobación humana de thumbnail/social hero por decisión del propietario.
- [x] CI/merge protegido excluidos del alcance; smoke post-deployment ejecutado contra Databricks.
- [ ] Completar formulario de challenge y congelar submission package.

## Criterio final de salida

El proyecto puede marcarse `READY_TO_SUBMIT` cuando las casillas técnicas estén en PASS; el formulario y la confirmación de enlaces son acciones externas de envío. La implementación local actual queda en `ENGINEERING_COMPLETE_SUBMISSION_FORM_PENDING`.
