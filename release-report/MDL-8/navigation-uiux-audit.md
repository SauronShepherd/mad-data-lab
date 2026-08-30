# MDL-8 — Auditoría funcional, navegación y UI/UX

Fecha: 2026-08-29

## Alcance

Se inventariaron las rutas públicas `/`, `/library`, `/articles`, `/groups`, `/variants`, `/feedback`, `/comments`, `/account` y `/admin`. La matriz de Playwright cubre escritorio (1440×900), tablet (1024×768) y móvil (390×844), con persistencia de idioma/tema, guardado local, feedback, comentarios, suscripción, administración y eliminación de la entrada `Apache Spark WTF???`.

## Estado verificado

- Compilación Vite: PASS.
- TypeScript: PASS.
- Traducción de las ocho superficies públicas: implementada y cubierta por prueba.
- Deep links públicos servidos por FastAPI: implementados.
- Feedback y comentarios: guardado local explícito, sin fingir persistencia de servidor.
- Suscripción: control visible, checkout deliberadamente no habilitado en esta release candidata.
- Aprobaciones humanas: excluidas del criterio de finalización por decisión del propietario.

## Diagnóstico automático

El arnés mide:

1. `scrollWidth > innerWidth` para detectar overflow horizontal.
2. Elementos interactivos fuera del viewport horizontal.
3. Imágenes incompletas o con `naturalWidth === 0`.
4. Botones habilitados sin etiqueta ni texto.
5. Contraste básico y coherencia visual: revisión de tokens/clases y comprobación manual pendiente de automatización cromática completa.

## Resultado del recorrido

Tras corregir el uso de `networkidle` por readiness DOM y locators semánticos, el recorrido completo terminó correctamente. Se generaron 57 capturas: 19 para cada viewport (escritorio, tablet y móvil), incluyendo landing, tablero, briefing, cinco experimentos, veredicto, debrief y las ocho rutas públicas.

El diagnóstico produjo `PASS` en los tres viewports: sin overflow horizontal, sin elementos fuera de pantalla, sin imágenes rotas y sin botones habilitados sin texto o etiqueta.

## Corrección requerida antes del cierre técnico

- El recorrido local y remoto están cerrados. La ejecución remota autenticada completó el flujo live Genie en desktop, tablet y móvil con timeout operativo de 300 segundos por acción.
- Sustituir la revisión cromática manual por una medición WCAG automatizada: completado; axe `color-contrast` pasa en los tres viewports.

## Criterio de aceptación

La aplicación no debe declararse 100% terminada mientras el recorrido visual completo no produzca evidencias para cada pantalla y acción en los tres viewports y el diagnóstico no sea `PASS` en todas las dimensiones.
