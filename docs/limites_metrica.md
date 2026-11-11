
# Límites de la métrica de evaluación de respuestas

## 1. ¿Qué mide la métrica?

El proyecto utiliza precisión, cobertura y F1 para comparar las respuestas generadas por el modelo con respuestas de referencia.

- **Precisión:** proporción de palabras de la respuesta generada que coinciden con la referencia.
- **Cobertura:** proporción de palabras de la referencia que aparecen en la respuesta generada.
- **F1:** combina precisión y cobertura mediante su media armónica.

Estas métricas permiten medir coincidencias entre palabras, pero no evalúan directamente si una respuesta es correcta, útil o adecuada para el contexto de la consulta.

## 2. Limitaciones y fallos identificados

La revisión manual de 10 casos permitió identificar las siguientes limitaciones:

### 2.1. Respuestas extensas penalizadas

Una respuesta puede cubrir correctamente los elementos de la referencia y, aun así, obtener una precisión baja cuando incorpora explicaciones, ejemplos y recomendaciones adicionales.

**Caso observado:** "¿Cómo mejorar la rentabilidad de una pequeña pastelería?" obtuvo un F1 de 0.0269. Sin embargo, la revisión manual determinó que abordaba el control de costos, la reducción de mermas, la optimización de compras, los precios y la priorización de productos rentables.

### 2.2. Diferencias de vocabulario

La métrica depende de la coincidencia literal de palabras. Puede penalizar respuestas que expresan una misma idea utilizando términos diferentes.

Por ejemplo, una respuesta puede explicar el control de existencias sin utilizar exactamente la expresión "niveles mínimos de stock".

### 2.3. Dificultad para reconocer el contexto

La métrica no determina si la respuesta está adaptada al contexto de la pregunta.

**Caso observado:** "¿Cómo organizar las compras de ingredientes?" obtuvo un F1 de 0.0304. La respuesta se enfocó principalmente en compras domésticas y planificación de comidas, en lugar de abordar la gestión de compras de una pastelería.

### 2.4. No evalúa directamente la veracidad

La coincidencia de palabras no garantiza que la información sea correcta. Tampoco permite identificar por sí sola afirmaciones contradictorias o datos incorrectos.

Por esta razón, se requiere una revisión cualitativa adicional.

## 3. Tamaño de muestra y criterios de selección

Se trabajó con un conjunto de 20 respuestas generadas por el modelo.

Para la revisión manual se seleccionaron 10 casos:

- Los 5 casos con menor valor F1.
- Los 5 casos con mayor valor F1.

Cada respuesta se evaluó mediante tres criterios:

1. **Corrección factual:** determina si los datos y afirmaciones coinciden con la referencia.
2. **Completitud:** determina si la respuesta incluye los elementos importantes de la referencia.
3. **Contradicción:** identifica si la respuesta afirma algo opuesto a la referencia.

Resultados de la revisión:

- Casos revisados: 10.
- Casos completos y sin contradicciones: 8.
- Casos con evaluación parcial: 2.
- Casos con contradicciones identificadas: 0.

La muestra fue seleccionada intencionalmente a partir de los extremos de F1, por lo que no representa necesariamente el comportamiento de todas las respuestas del sistema.

## 4. Recomendaciones de uso

La métrica debe utilizarse como una herramienta de apoyo y no como único criterio para determinar la calidad de una respuesta.

Se recomienda:

- Utilizar precisión, cobertura y F1 para comparar coincidencias textuales.
- Complementar los resultados con revisión cualitativa.
- Revisar especialmente respuestas con valores F1 muy bajos.
- Comprobar manualmente las respuestas que incluyan cifras, fechas, nombres o afirmaciones relevantes.
- Mejorar las respuestas de referencia para que representen adecuadamente el contexto de las consultas.
- No interpretar un F1 alto como garantía de veracidad ni un F1 bajo como prueba automática de una respuesta incorrecta.

## Conclusión

La evaluación realizada demuestra que las métricas basadas en coincidencia textual tienen limitaciones para evaluar respuestas generadas por modelos de lenguaje.

En los 10 casos revisados, se observaron respuestas completas que obtuvieron valores F1 bajos debido a diferencias de extensión y vocabulario. También se identificaron respuestas que no se ajustaban al contexto de la consulta.

Por lo tanto, para evaluar adecuadamente PymeCopilot AI es necesario combinar métricas automáticas con criterios de revisión humana.
