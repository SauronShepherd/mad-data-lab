# MAD DATA LAB — estado real y plan exhaustivo de construcción y pruebas

Fecha de auditoría: 2026-08-29  
Alcance: MDL-1 a MDL-8, aplicación local y despliegue Databricks.

## 1. Resumen ejecutivo

La base funcional está avanzada y el runtime desplegado está operativo. El código ya contiene el dominio canónico, Case #042 determinista, orquestación de cinco experimentos, scoring server-authoritative, exploración de evidencia, recuperación de sesión, rutas públicas, preferencias y un recorrido responsive instrumentado.

No debe confundirse `PASS` de una prueba con “producto terminado” en todas las dimensiones. Las brechas técnicas principales son: automatización WCAG de contraste, revalidación final de la identidad exacta desplegada, persistencia backend de feedback/comentarios, integración real de suscripción, revisión de placeholders/enlaces del artículo, paquete final y pruebas live completas de Genie/warehouse. CI, branch protection y aprobaciones humanas están fuera del alcance por decisión explícita del propietario.

## 2. Inventario de rutas y superficies

### Rutas públicas

`/`, `/library`, `/articles`, `/groups`, `/variants`, `/feedback`, `/comments`, `/account`, `/admin`.

### Flujo jugable

Landing → Case Board → Briefing → Investigation → cinco experimentos → exploración de Record/Lineage/DQ → predicción final → Verdict → Debrief.

### Controles y estados transversales

Idioma EN/ES, tema lab/high-contrast, audio on/off, reduced motion, hints, Dr. Genie, recuperación de sesión, guardado de progreso, feedback, comentarios, suscripción, deep links, errores API, loading, expiración e idempotencia.

## 3. Estado por fase

| Fase | Estado | Evidencia | Brecha real |
|---|---|---|---|
| MDL-1 | Implementado/verificado | dominio, modelos, contratos, trazabilidad | Revalidar SHA contra identidad final |
| MDL-2 | Implementado/verificado | fixtures, DDL, generator, SQL registry, exclusión de truth | Seed/rollback productivo si se exige warehouse real |
| MDL-3 | Implementado local; live condicionado | contrato estricto, benchmark, boundary, circuit breaker | Soak/live Genie con identidad y configuración finales |
| MDL-4 | Implementado/verificado | estados, scoring, badges, verdict/debrief, replay | Reejecutar con source/deployment final |
| MDL-5 | Implementado/verificado | instrumentos, evidencia, teclado, audio, responsive | Contraste automatizado WCAG; revisión de contenido visual |
| MDL-6 | Implementado/verificado | errores, request IDs, resiliencia, seguridad, suite Python/browser | Repetición final sin procesos reutilizados |
| MDL-7 | Parcialmente cerrado | build, typecheck, smoke, soak y deployment | Ejecutar release candidate final y congelar hashes |
| MDL-8 | Parcialmente cerrado | capturas 57, diagnóstico responsive, rutas públicas | paquete, vídeo/enlaces/artículo y formulario externo |

## 4. Trabajo de construcción pendiente, en orden

### Bloque A — Baseline y reproducibilidad

1. Congelar commit/source identity.
2. Ejecutar `git diff --check` y registrar el SHA del checkout.
3. Ejecutar build frontend y guardar nombres/hash de assets.
4. Ejecutar `compileall`, typecheck y suite Python.
5. Ejecutar validadores MDL-1/2/3 en modo estricto.
6. Generar manifiesto con rutas, tamaño, hash y exclusiones.
7. Verificar que el manifiesto no incluye truth privada, credenciales, tokens, `node_modules`, temporales ni resultados obsoletos.

### Bloque B — API y dominio

1. Probar catálogo: Case válido, Case desconocido, estado de disponibilidad y bloqueo.
2. Probar creación idempotente con la misma clave y claves distintas.
3. Probar transiciones válidas e inválidas de cada estado.
4. Probar orden exacto de los cinco experimentos y rechazo de IDs no registrados.
5. Probar predicción inicial y final, incluyendo valores inválidos, repetición y early reveal.
6. Probar inspección de las tres capacidades de evidencia y rechazo de capacidades no desbloqueadas.
7. Probar conclusión incompleta, conclusión completa, score oculto durante investigación y score revelado después.
8. Probar debrief, badges, replay y recuperación de sesión.
9. Probar expiración TTL, restart y pérdida de sesión.
10. Probar errores 404/409/410/422/503 con envelope, `code`, `retryable` y `X-Request-ID`.
11. Probar concurrencia sobre la misma sesión y replay idempotente.
12. Confirmar que truth privada nunca aparece en respuestas, logs ni prompts.

### Bloque C — Genie y datos

1. Ejecutar contrato estricto MDL-3.
2. Ejecutar benchmark determinista.
3. Ejecutar live Genie con `GENIE_SPACE_ID` y configuración final.
4. Verificar que Genie solo recibe contexto permitido.
5. Probar prompt injection, output malformado, experimento no registrado y respuesta tardía.
6. Probar circuit breaker: apertura, cooldown y recuperación.
7. Ejecutar soak con concurrencia controlada y límites de latencia.
8. Ejecutar verificación remota de datos: 23 modified, 2 removed, 5 added, 14 unchanged, DQ no aditiva y ausencia de `CASE_TRUTH`.
9. Ejecutar seed/rollback solo si el warehouse de producción forma parte del alcance de entrega; registrar resultado y responsable técnico.

### Bloque D — Frontend funcional

1. Verificar cada transición del flujo con locator semántico.
2. Verificar que todos los botones tienen efecto observable, estado disabled correcto y feedback de error.
3. Verificar loading durante llamadas lentas y que no se habiliten acciones prematuramente.
4. Verificar idioma EN/ES en todas las rutas, tras navegación y reload.
5. Verificar tema y reduced motion tras reload.
6. Verificar audio bloqueado por el navegador sin bloquear el juego.
7. Verificar localStorage corrupto, ausente y valores desconocidos.
8. Verificar feedback/comentarios locales, límites y mensajes traducidos.
9. Verificar suscripción: control visible, mensaje honesto y ausencia de falsa transacción.
10. Verificar administración sin exponer información privada.
11. Verificar deep links directos y refresh en cada ruta pública.
12. Verificar ausencia total de `Apache Spark WTF???`.

### Bloque E — UI/UX y accesibilidad

1. Ejecutar cada flujo en 1440×900, 1024×768 y 390×844.
2. Capturar landing, cada pantalla de juego, cada acción de evidencia y cada ruta pública.
3. Medir overflow horizontal (`scrollWidth > innerWidth`).
4. Medir elementos interactivos fuera del viewport.
5. Verificar imágenes cargadas y dimensiones naturales.
6. Verificar botones sin texto, nombre accesible o label.
7. Ejecutar axe-core y corregir critical/serious.
8. Automatizar contraste WCAG AA de texto normal, texto grande, controles y estados disabled.
9. Verificar foco visible, orden de tabulación, escape de diálogos, labels y mensajes live.
10. Verificar touch target mínimo y ausencia de solapamiento en móvil.
11. Verificar consistencia de tipografía, colores, bordes, estados y espaciado frente a tokens/UIX.
12. Revisar visualmente una muestra de cada viewport y documentar cualquier desviación como bug o decisión.

### Bloque F — Release y submission

1. Ejecutar `release_candidate.py` sobre source identity final.
2. Ejecutar smoke remoto y soak remoto con el deployment final.
3. Regenerar screenshots, `ui-diagnostic.json`, informes y hashes.
4. Sustituir placeholders del artículo por assets/enlaces definitivos disponibles.
5. Generar/revisar vídeo demo: duración, resolución, audio, narrativa y ausencia de datos privados.
6. Validar URL pública, deep links, health y assets remotos.
7. Construir ZIP final desde el manifiesto, contar entradas, comprobar hashes y volver a abrirlo.
8. Registrar `deployment_id`, source path, app state y compute state.
9. Separar claramente PASS técnico de acciones externas: formulario y confirmación de enlaces.
10. Congelar artefactos y no modificar código después sin repetir el bloque A.

## 5. Matriz de pruebas mínima

| Suite | Local | Remota | Viewports | Criterio |
|---|---:|---:|---|---|
| Python dominio/API | sí | opcional | n/a | 100% pass, skips explicados |
| Typecheck/build | sí | n/a | n/a | exit code 0 |
| MDL-3 strict | sí | sí | n/a | contrato y boundary pass |
| Flujo completo | sí | sí | desktop/tablet/mobile | todas las transiciones y capturas |
| Rutas públicas | sí | sí | desktop/tablet/mobile | 8/8 rutas, deep link y reload |
| Preferencias | sí | sí | desktop/tablet/mobile | idioma, tema, audio, motion persistentes |
| Evidencia | sí | sí | desktop/tablet/mobile | record, lineage, DQ y score correcto |
| Resiliencia | sí | sí | n/a | errores y recuperación verificables |
| Seguridad | sí | sí | n/a | truth/secretos no filtrados |
| UI/UX | sí | sí | desktop/tablet/mobile | overflow/offscreen/images/buttons/axe/contrast pass |
| Release | sí | sí | n/a | manifiesto, ZIP, vídeo y hashes consistentes |

## 6. Definición de terminado

Se puede declarar `READY_TO_SUBMIT` cuando:

- todas las suites técnicas tienen resultado PASS o skip justificado;
- el deployment final coincide con el source identity auditado;
- existen capturas para cada pantalla y acción en los tres viewports;
- `ui-diagnostic.json` es PASS y el contraste WCAG está automatizado;
- no hay fallos funcionales abiertos de severidad crítica, alta o media;
- el ZIP final es reproducible y su manifiesto coincide con el contenido;
- el artículo y vídeo no contienen placeholders ni secretos;
- las acciones externas se listan aparte y no se presentan como aprobaciones humanas requeridas.

## 7. Riesgos y decisiones

- Feedback/comentarios actuales son locales; no deben venderse como colaboración persistente multiusuario hasta implementar backend, identidad, moderación, retención y pruebas.
- Suscripción no es una integración de pagos; el botón debe seguir comunicándolo explícitamente.
- `contrastBasic: manual-review` no equivale a PASS WCAG; debe eliminarse esa ambigüedad.
- Un smoke remoto de rutas públicas no sustituye el flujo autenticado live Genie.
- CI no forma parte del criterio de salida por instrucción del propietario.
- No existe gate de aprobación humana; el control de calidad visual será técnico y documentado.
