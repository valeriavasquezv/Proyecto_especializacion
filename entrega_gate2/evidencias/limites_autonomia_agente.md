# Límites de autonomía y supervisión humana del agente PymeCopilot AI

## 1. Clasificación de herramientas según nivel de riesgo

El agente financiero dispone de las siguientes herramientas:

| Herramienta | Función | Nivel de riesgo |
|---|---|---|
| `calcular_indicadores_financieros` | Calcula utilidad, margen y proporciones de costos y gastos. | Bajo |
| `consultar_conceptos_financieros` | Consulta definiciones de conceptos financieros. | Bajo |

Ambas herramientas realizan operaciones de consulta y cálculo. No ejecutan transacciones económicas ni modifican información externa.

## 2. Herramientas que requieren aprobación humana

Actualmente, ninguna herramienta requiere aprobación humana previa, debido a que sus operaciones son de bajo riesgo.

El agente no tiene autorización para ejecutar transferencias, realizar pagos, emitir reembolsos, cancelar pedidos ni modificar registros financieros externos.

Si en futuras versiones se incorporan herramientas que puedan generar consecuencias económicas o cambios irreversibles, deberán incorporar un mecanismo de aprobación humana antes de su ejecución.

## 3. Trazabilidad y patrones sospechosos

El sistema registra las interacciones en el archivo `trazas_agente.jsonl`, utilizando el formato JSON Lines.

Cada registro contiene:
- Fecha y hora de ejecución.
- Identificador de sesión.
- Consulta del usuario.
- Herramientas utilizadas.
- Argumentos enviados a cada herramienta.
- Observaciones o resultados obtenidos.
- Respuesta final del agente.

Se consideran patrones que requieren revisión:

- Uso consecutivo e inesperado de una misma herramienta.
- Argumentos incorrectos o inconsistentes.
- Respuestas finales que no estén respaldadas por los resultados de las herramientas.
- Ejecución de herramientas de alto riesgo sin una aprobación registrada, si estas se incorporan en el futuro.

Se propone revisar semanalmente una muestra de las trazas y revisar todas las ejecuciones de herramientas de alto riesgo cuando existan.

El proyecto cuenta con la función `marcar_repeticiones_sospechosas()` para identificar usos consecutivos de una misma herramienta dentro de una interacción.

## 4. Plan de actuación ante comportamientos inesperados

Si el agente presenta un comportamiento inesperado, se seguirá este procedimiento:

1. Detener temporalmente la ejecución del agente o deshabilitar la herramienta involucrada.
2. Revisar el registro correspondiente en `trazas_agente.jsonl`.
3. Identificar la consulta, los argumentos enviados y el resultado obtenido.
4. Revisar las instrucciones del agente, la descripción de la herramienta y su esquema de parámetros.
5. Corregir el problema y ejecutar pruebas controladas.
6. Habilitar nuevamente la herramienta después de verificar que funciona correctamente.

## 5. Límites actuales del agente

PymeCopilot AI funciona como un asistente de análisis y gestión financiera. Sus herramientas actuales permiten realizar cálculos y consultar conceptos financieros.

El agente no reemplaza la revisión de un profesional financiero ni tiene autonomía para ejecutar operaciones económicas externas.

Cualquier ampliación futura de sus capacidades deberá considerar una nueva evaluación de riesgos y mecanismos de supervisión humana adecuados.