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

import os

if os.path.exists("resultados_metricas.json"):
    with open("resultados_metricas.json", "r", encoding="utf-8") as archivo:
        resultados = json.load(archivo)
else:
    resultados = []

consultas_existentes = {r["consulta"] for r in resultados}

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
    },
    {
        "consulta": "¿Cómo calcular el costo de una receta de pastelería?",
        "referencia": "Se deben calcular las cantidades utilizadas de cada ingrediente y multiplicarlas por su costo unitario."
    },
    {
        "consulta": "¿Cómo calcular el costo de la mano de obra en una pastelería?",
        "referencia": "Se debe multiplicar el tiempo trabajado por el costo de la hora de trabajo."
    },
    {
        "consulta": "¿Qué gastos indirectos debe considerar una pastelería?",
        "referencia": "Debe considerar electricidad, agua, gas, arriendo, limpieza y mantenimiento de equipos."
    },
    {
        "consulta": "¿Cómo calcular el margen de utilidad de un producto?",
        "referencia": "El margen de utilidad se calcula comparando la ganancia obtenida con el precio de venta."
    },
    {
        "consulta": "¿Cómo determinar el punto de equilibrio de una pastelería?",
        "referencia": "Se dividen los costos fijos por el margen de contribución unitario para determinar las unidades necesarias para cubrir los costos."
    },
    {
        "consulta": "¿Cómo reducir las mermas de ingredientes?",
        "referencia": "Se deben estandarizar recetas, controlar cantidades, registrar desperdicios y revisar los procesos de producción."
    },
    {
        "consulta": "¿Cómo organizar las compras de ingredientes?",
        "referencia": "Se deben revisar las existencias, establecer niveles mínimos de stock y planificar las compras según la demanda."
    },
    {
        "consulta": "¿Qué información debe contener una ficha técnica de producto?",
        "referencia": "Debe incluir ingredientes, cantidades, procedimiento, rendimiento, costos y características del producto."
    },
    {
        "consulta": "¿Cómo calcular el costo unitario de un producto?",
        "referencia": "Se divide el costo total de producción por la cantidad de unidades producidas."
    },
    {
        "consulta": "¿Cómo registrar las ventas diarias de una pastelería?",
        "referencia": "Se debe registrar la fecha, producto vendido, cantidad, precio unitario, total y medio de pago."
    },
    {
        "consulta": "¿Por qué es importante separar las finanzas personales y del negocio?",
        "referencia": "Permite conocer la rentabilidad real del negocio, controlar los gastos y evitar confundir el dinero personal con el empresarial."
    },
    {
        "consulta": "¿Cómo identificar los productos más rentables de una pastelería?",
        "referencia": "Se deben comparar las ventas, los costos de producción y los márgenes de utilidad de cada producto."
    },
    {
        "consulta": "¿Cómo planificar la producción de una pastelería?",
        "referencia": "Se debe considerar la demanda estimada, las ventas históricas, la capacidad productiva y la disponibilidad de ingredientes."
    },
    {
        "consulta": "¿Cómo controlar las fechas de vencimiento de los ingredientes?",
        "referencia": "Se deben registrar las fechas de vencimiento, etiquetar los productos y utilizar primero los ingredientes que vencen antes."
    },
    {
        "consulta": "¿Qué indicadores debería revisar una pastelería?",
        "referencia": "Debe revisar ventas, costos, margen de utilidad, inventario, mermas y rentabilidad."
    },
    {
        "consulta": "¿Cómo evaluar si conviene ofrecer un nuevo producto?",
        "referencia": "Se deben analizar la demanda potencial, los costos, el precio de venta, la competencia y la rentabilidad esperada."
    },
    {
        "consulta": "¿Cómo mejorar la rentabilidad de una pequeña pastelería?",
        "referencia": "Se puede mejorar controlando costos, reduciendo mermas, optimizando compras, ajustando precios y priorizando productos rentables."
    }
]
print("\nTOTAL DE CASOS:", len(casos))
print("CONSULTAS NUEVAS:", len(casos) - len(consultas_existentes))

for caso in casos:
    print(caso["consulta"])

for caso in casos:

    pregunta = caso["consulta"]
    referencia = caso["referencia"]

    if pregunta in consultas_existentes:
        print(f"Ya existe, se omite: {pregunta}")
        continue

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
        "referencia": referencia,
        "respuesta": respuesta,
        "precision": metricas["precision"],
        "cobertura": metricas["cobertura"],
        "f1": metricas["f1"]
    }

    resultados.append(registro)
    consultas_existentes.add(pregunta)

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