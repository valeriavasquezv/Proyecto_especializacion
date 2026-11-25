# Decision de personalizacion

## 1. El problema
PymeCopilot AI busca ofrecer asesoría financiera a las PYMEs, analizando sus datos reales de ventas, costos, gastos y flujo de caja. El sistema necesita consultar información actualizada de cada negocio para entregar respuestas y recomendaciones financieras contextualizadas.

## 2. Resultado del metodo de decision
- RAG: 5 puntos
- PEFT: 1 punto
- Fine-tuning completo: 0 puntos

## 3. Tecnica elegida y por que

RAG es la estrategia más adecuada para PymeCopilot AI porque permite consultar información financiera actualizada de cada PYME sin necesidad de reentrenar el modelo cada vez que cambian sus ventas, costos, gastos o deudas.

Además, permite recuperar información específica del negocio para generar respuestas y recomendaciones financieras contextualizadas. Frente al fine-tuning completo y PEFT, RAG resulta más conveniente en esta etapa porque contamos con un presupuesto limitado para realizar entrenamientos y todavía no disponemos de un dataset suficientemente grande y validado.

La elección de RAG no implica descartar futuras técnicas de personalización. En una etapa posterior podríamos evaluar PEFT si detectamos problemas comprobados de formato, tono o comportamiento.

RAG complementará los módulos de cálculo financiero del sistema. Los indicadores como rentabilidad, margen, flujo de caja y punto de equilibrio deberán calcularse mediante funciones verificables, utilizando los datos recuperados del negocio.

## 4. Que necesitarias para ejecutarla

Para implementar RAG en PymeCopilot AI necesitamos construir y mantener un corpus de información financiera que permita recuperar antecedentes relevantes para responder las consultas de cada PYME.

El corpus deberá considerar:

- Documentación financiera y administrativa de referencia.
- Registros de ventas, costos, gastos, pagos y deudas de cada negocio.
- Información histórica y actualizada del flujo de caja.
- Documentación de apoyo para interpretar indicadores financieros.

También necesitamos preparar los documentos y datos para su indexación, generar embeddings y almacenarlos en Chroma, que funcionará como nuestra base vectorial.

La arquitectura deberá garantizar la separación lógica de la información de cada PYME, de modo que las consultas de un negocio nunca recuperen datos pertenecientes a otro.

El proyecto ya cuenta con avances en la implementación de embeddings, Chroma e indexación de documentos. Sin embargo, todavía debemos ampliar y organizar el corpus financiero, definir cómo se incorporarán los datos particulares de cada PYME y mantener actualizado el índice.

Finalmente, necesitaremos validar la calidad de la recuperación, controlar la latencia y asegurar que los datos de cada negocio se mantengan separados y protegidos.
