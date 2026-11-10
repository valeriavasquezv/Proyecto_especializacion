import json
from src.cliente import consultar_modelo
from src.metricas_texto import calcular_metricas

def resumir_metricas(resultados):

    if not resultados:
        return {
            "precision_promedio": 0,
            "cobertura_promedio": 0,
            "f1_promedio": 0
        }

    n = len(resultados)

    return {
        "precision_promedio": sum(
            r["precision"] for r in resultados
        ) / n,

        "cobertura_promedio": sum(
            r["cobertura"] for r in resultados
        ) / n,

        "f1_promedio": sum(
            r["f1"] for r in resultados
        ) / n
    }

resultados = []

casos = [
    {
        "consulta": "¿Qué elementos debo considerar para calcular el costo de producción de una torta?",
        "referencia": "Para calcular el costo de producción se deben considerar ingredientes, cantidades utilizadas, mano de obra y costos indirectos como electricidad, gas y agua."
    },
    {
        "consulta": "¿Cómo calcular el precio de venta de una torta?",
        "referencia": "El precio de venta se calcula sumando el costo total de producción y el margen de utilidad deseado."
    },
    {
        "consulta": "¿Cómo controlar el inventario de ingredientes de una pastelería?",
        "referencia": "Se debe registrar cada ingrediente, las cantidades disponibles, el consumo, el stock mínimo y las necesidades de reposición."
    }
]

for caso in casos:
    print(caso["consulta"])

for caso in casos:

    pregunta = caso["consulta"]
    referencia = caso["referencia"]

    try:
        respuesta = consultar_modelo(pregunta)
    except RuntimeError as error:
        print(f"No fue posible evaluar: {pregunta}")
        print(error)
        continue

    print("\nRESPUESTA DE GEMINI:")
    print(respuesta)

    metricas = calcular_metricas(referencia, respuesta)

    registro = {
        "consulta": pregunta,
        "respuesta": respuesta,
        "precision": metricas["precision"],
        "cobertura": metricas["cobertura"],
        "f1": metricas["f1"]
    }

    resultados.append(registro)

    print("\nMÉTRICAS:")
    print(metricas)

resumen = resumir_metricas(resultados)

print("\nRESUMEN DE MÉTRICAS:")
print(resumen)

with open("resultados_metricas.json", "w", encoding="utf-8") as archivo:
    json.dump(
        resultados,
        archivo,
        indent=2,
        ensure_ascii=False
    )

peores_casos = sorted(
    resultados,
    key=lambda r: r["f1"]
)

print("\nLOS 3 PEORES CASOS:")

for caso in peores_casos[:3]:
    print(caso["consulta"], caso["f1"])