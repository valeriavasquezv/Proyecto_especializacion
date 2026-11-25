
def recomendar_estrategia(respuestas):
    puntos = {
        "RAG": 0,
        "Fine-tuning completo": 0,
        "PEFT": 0
    }

    if respuestas["informacion_cambia_seguido"]:
        puntos["RAG"] += 3

    if respuestas["problema_de_formato_o_tono"]:
        puntos["PEFT"] += 2
        puntos["Fine-tuning completo"] += 1

    if respuestas["dataset_grande_y_de_calidad"]:
        puntos["Fine-tuning completo"] += 2
        puntos["PEFT"] += 1

    if respuestas["presupuesto_limitado_o_iterar_rapido"]:
        puntos["RAG"] += 2
        puntos["PEFT"] += 1

    if respuestas["necesita_multiples_variantes"]:
        puntos["PEFT"] += 2

    maximo = max(puntos.values())

    ganadoras = [
        tecnica
        for tecnica, puntaje in puntos.items()
        if puntaje == maximo
    ]

    return puntos, ganadoras


respuestas_mi_caso = {
    "informacion_cambia_seguido": True,
    "problema_de_formato_o_tono": False,
    "dataset_grande_y_de_calidad": False,
    "presupuesto_limitado_o_iterar_rapido": True,
    "necesita_multiples_variantes": False,
}


if any(valor is None for valor in respuestas_mi_caso.values()):
    raise SystemExit(
        "Completa las cinco respuestas con True o False antes de continuar."
    )

puntos, ganadoras = recomendar_estrategia(respuestas_mi_caso)

print("Puntajes:", puntos)
print("Estrategia recomendada:", ganadoras)


def generar_esqueleto_decision(problema, puntos, ganadoras):
    empate = len(ganadoras) > 1
    lineas = []

    lineas.append("# Decision de personalizacion")
    lineas.append("")

    lineas.append("## 1. El problema")
    lineas.append(problema)
    lineas.append("")

    lineas.append("## 2. Resultado del metodo de decision")

    for tecnica, puntaje in sorted(
        puntos.items(),
        key=lambda x: -x[1]
    ):
        lineas.append(f"- {tecnica}: {puntaje} puntos")

    if empate:
        lineas.append("")
        lineas.append(f"**Empate entre: {', '.join(ganadoras)}**")

    lineas.append("")
    lineas.append("## 3. Tecnica elegida y por que")
    lineas.append(
        f"[COMPLETAR: por que {ganadoras[0]} responde mejor a este caso]"
    )

    lineas.append("")
    lineas.append("## 4. Que necesitarias para ejecutarla")
    lineas.append(
        "[COMPLETAR: corpus faltante, datos y recursos necesarios]"
    )

    return "\n".join(lineas)


problema = (
    "PymeCopilot AI busca ofrecer asesoría financiera a las PYMEs, "
    "analizando sus datos reales de ventas, costos, gastos y flujo de caja. "
    "El sistema necesita consultar información actualizada de cada negocio "
    "para entregar respuestas y recomendaciones financieras contextualizadas."
)

esqueleto = generar_esqueleto_decision(
    problema,
    puntos,
    ganadoras
)

print(esqueleto)

with open("decision_personalizacion.md", "w", encoding="utf-8") as archivo:
    archivo.write(esqueleto)

print("\nDocumento generado correctamente.")
