
revision_manual = [
    {
        "consulta": "¿Qué información debe contener una ficha técnica de producto?",
        "f1": 0.0231,
        "correccion_factual": "Parcial",
        "completitud": "No",
        "contradiccion": "No",
        "justificacion": "La respuesta describe una ficha técnica general, pero omite elementos esenciales para una ficha de producción de pastelería: cantidades, procedimiento, rendimiento y costos."
    },
    {
        "consulta": "¿Cómo mejorar la rentabilidad de una pequeña pastelería?",
        "f1": 0.0269,
        "correccion_factual": "Sí",
        "completitud": "Sí",
        "contradiccion": "No",
        "justificacion": "Aborda el control de costos, reducción de desperdicios, optimización de compras, precios y priorización de productos rentables."
    },
    {
        "consulta": "¿Cómo organizar las compras de ingredientes?",
        "f1": 0.0304,
        "correccion_factual": "Parcial",
        "completitud": "No",
        "contradiccion": "No",
        "justificacion": "La respuesta se enfoca principalmente en compras domésticas y planificación de comidas. No desarrolla suficientemente el stock mínimo ni la planificación de compras según la demanda de una pastelería."
    },
    {
        "consulta": "¿Qué gastos indirectos debe considerar una pastelería?",
        "f1": 0.0322,
        "correccion_factual": "Sí",
        "completitud": "Sí",
        "contradiccion": "No",
        "justificacion": "Incluye electricidad, agua, gas, arriendo, limpieza y mantenimiento de equipos, además de otros gastos."
    },
    {
        "consulta": "¿Qué indicadores debería revisar una pastelería?",
        "f1": 0.0324,
        "correccion_factual": "Sí",
        "completitud": "Sí",
        "contradiccion": "No",
        "justificacion": "Incluye ventas, costos, margen, inventario, mermas y rentabilidad mediante distintos indicadores operativos y financieros."
    },
    {
        "consulta": "¿Cómo calcular el precio de venta de una torta?",
        "f1": 0.0527,
        "correccion_factual": "Sí",
        "completitud": "Sí",
        "contradiccion": "No",
        "justificacion": "Explica que el precio se obtiene considerando el costo total de producción y la utilidad deseada."
    },
    {
        "consulta": "¿Cómo calcular el margen de utilidad de un producto?",
        "f1": 0.0542,
        "correccion_factual": "Sí",
        "completitud": "Sí",
        "contradiccion": "No",
        "justificacion": "Presenta la fórmula que compara la ganancia con el precio de venta y desarrolla un ejemplo numérico."
    },
    {
        "consulta": "¿Cómo calcular el costo unitario de un producto?",
        "f1": 0.0582,
        "correccion_factual": "Sí",
        "completitud": "Sí",
        "contradiccion": "No",
        "justificacion": "Explica la división del costo total de producción por la cantidad de unidades producidas."
    },
    {
        "consulta": "¿Cómo determinar el punto de equilibrio de una pastelería?",
        "f1": 0.0622,
        "correccion_factual": "Sí",
        "completitud": "Sí",
        "contradiccion": "No",
        "justificacion": "Presenta la fórmula de costos fijos divididos por el margen de contribución unitario y desarrolla un ejemplo."
    },
    {
        "consulta": "¿Qué elementos debo considerar para calcular el costo de producción de una torta?",
        "f1": 0.0675,
        "correccion_factual": "Sí",
        "completitud": "Sí",
        "contradiccion": "No",
        "justificacion": "Considera ingredientes, cantidades utilizadas, mano de obra y costos indirectos como electricidad, gas y agua."
    }
]

import json

with open("revision_manual.json", "w", encoding="utf-8") as archivo:
    json.dump(revision_manual, archivo, indent=2, ensure_ascii=False)

print("Revisión manual guardada correctamente.")
print(f"Total de casos revisados: {len(revision_manual)}")
