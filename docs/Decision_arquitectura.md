# Decisión de arquitectura: elección de modelo

## 1. Modelo elegido

Se selecciona provisionalmente **`gemini-3.1-flash-lite`** para la miniaplicación.

La decisión prioriza el menor costo por solicitud, considerando que el modelo respondió correctamente a la pregunta de prueba utilizada. Esta elección podrá revisarse cuando se evalúe la calidad con más preguntas representativas.

## 2. Diagrama de arquitectura

Se utiliza el diagrama de arquitectura desarrollado en el Bloque 8, que representa el flujo de la miniaplicación para consumir la API de Gemini.

![Diagrama de arquitectura](<Arquitectura miniaplicación (Diagrama).png>)

## 3. Comparación de candidatos

Los siguientes resultados corresponden a cuatro solicitudes por modelo con la misma pregunta: «Explica en dos frases qué es una variable en Python».

| Indicador | `gemini-3.1-flash-lite` | `gemini-3.5-flash-lite` |
|---|---:|---:|
| Solicitudes exitosas | 4 de 4 | 4 de 4 |
| Latencia promedio | 10,06 segundos | 4,81 segundos |
| Costo promedio por solicitud | US$ 0,00008175 | US$ 0,00013798 |
| Calidad observada | Respuestas correctas y coherentes | Respuestas correctas y coherentes |

Los costos son estimaciones calculadas con los precios configurados en el código y los tokens reportados por la API. No representan una cotización de facturación.

La evaluación de calidad es preliminar, ya que se utilizó una sola pregunta. Los resultados de latencia corresponden a las ejecuciones realizadas y pueden variar en otras condiciones.

## 4. Justificación

Se selecciona `gemini-3.1-flash-lite` porque presentó el menor costo promedio por solicitud: aproximadamente US$ 0,00008175, frente a US$ 0,00013798 de `gemini-3.5-flash-lite`.

El segundo modelo fue más rápido, con una latencia promedio de 4,81 segundos frente a 10,06 segundos. Sin embargo, para esta evaluación inicial se prioriza el costo, ya que el primer modelo entregó respuestas correctas para la pregunta utilizada.

La decisión se basa en el equilibrio entre costo, latencia y calidad observada. Se requiere evaluar más preguntas antes de concluir que ambos modelos ofrecen una calidad equivalente.

## 5. Alternativa descartada y por qué

Se descarta provisionalmente `gemini-3.5-flash-lite`.

Aunque obtuvo una latencia promedio menor, su costo promedio por solicitud fue aproximadamente un 69 % superior al de `gemini-3.1-flash-lite`. Para la miniaplicación evaluada, esa diferencia de costo tiene mayor peso que la mejora de velocidad observada.

Esta alternativa podría reconsiderarse si futuras pruebas demuestran una mejora de calidad que justifique su costo adicional.

---

**Limitaciones de la evaluación:** los resultados se obtuvieron con una única pregunta de prueba y cuatro solicitudes exitosas por modelo. No se evaluaron todavía otros casos de uso ni el comportamiento con cargas mayores. La decisión es provisional y se basa en los datos disponibles al momento de la evaluación.