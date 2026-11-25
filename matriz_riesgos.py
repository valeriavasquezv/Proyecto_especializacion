def calcular_puntaje(probabilidad, impacto):
    if not (1 <= probabilidad <= 5):
        raise ValueError("La probabilidad debe estar entre 1 y 5.")

    if not (1 <= impacto <= 5):
        raise ValueError("El impacto debe estar entre 1 y 5.")

    return probabilidad * impacto


def clasificar_riesgo(puntaje):

    if puntaje >= 15:
        return "CRITICO"

    elif puntaje >= 9:
        return "ALTO"

    elif puntaje >= 4:
        return "MEDIO"

    return "BAJO"


def esta_al_limite(probabilidad, impacto):

    categoria_actual = clasificar_riesgo(
        calcular_puntaje(probabilidad, impacto)
    )

    # Revisar cambios de +/- 1 en probabilidad o impacto
    variaciones = [
        (probabilidad - 1, impacto),
        (probabilidad + 1, impacto),
        (probabilidad, impacto - 1),
        (probabilidad, impacto + 1)
    ]

    for nueva_probabilidad, nuevo_impacto in variaciones:

        if 1 <= nueva_probabilidad <= 5 and 1 <= nuevo_impacto <= 5:

            nueva_categoria = clasificar_riesgo(
                calcular_puntaje(
                    nueva_probabilidad,
                    nuevo_impacto
                )
            )

            if nueva_categoria != categoria_actual:
                return True

    return False

riesgos = [
    {
        "id": 1,
        "riesgo": "Inyección de instrucciones maliciosas en documentos recuperados por RAG",
        "probabilidad": 4,
        "impacto": 4,
        "mitigacion": "Aplicar filtro de patrones sospechosos y delimitar el contexto recuperado. (Bloque 31)",
        "supervision": "Revisar documentos sospechosos antes de incorporarlos al contexto del agente."
    },
    {
        "id": 2,
        "riesgo": "Error en el cálculo de indicadores financieros",
        "probabilidad": 3,
        "impacto": 5,
        "mitigacion": "Validar los cálculos mediante reglas deterministas y pruebas automatizadas.",
        "supervision": "Exigir revisión de los resultados financieros antes de utilizarlos para decisiones importantes."
    },
    {
        "id": 3,
        "riesgo": "Exposición de información financiera entre distintas PYMEs",
        "probabilidad": 2,
        "impacto": 5,
        "mitigacion": "Validar la identidad de la PYME y su contexto antes de recuperar información.",
        "supervision": "Revisar los permisos y registros de acceso entre organizaciones."
    },
    {
        "id": 4,
        "riesgo": "Generación de recomendaciones financieras con datos insuficientes",
        "probabilidad": 4,
        "impacto": 3,
        "mitigacion": "Solicitar datos faltantes y prohibir la invención de cifras mediante el prompt versionado. (Bloque 32)",
        "supervision": "Revisar las recomendaciones cuando falten antecedentes financieros relevantes."
    },
    {
        "id": 5,
        "riesgo": "Activación de una versión de prompt no validada",
        "probabilidad": 3,
        "impacto": 4,
        "mitigacion": "Implementar aprobación humana antes del despliegue mediante LangGraph. (Bloque 32)",
        "supervision": "Exigir aprobación explícita de una persona antes de activar cada nueva versión."
    }
]

def evaluar_riesgos():

    print("\n=== MATRIZ DE RIESGOS PYME COPILOT AI ===\n")

    for riesgo in riesgos:

        probabilidad = riesgo["probabilidad"]
        impacto = riesgo["impacto"]

        puntaje = calcular_puntaje(probabilidad, impacto)
        categoria = clasificar_riesgo(puntaje)
        limite = esta_al_limite(probabilidad, impacto)

        print(f"\nRiesgo {riesgo['id']}: {riesgo['riesgo']}")
        print(f"Probabilidad: {probabilidad}")
        print(f"Impacto: {impacto}")
        print(f"Puntaje: {puntaje}")
        print(f"Categoría: {categoria}")

        if limite:
            print("AL LIMITE")

        print(f"Mitigación: {riesgo['mitigacion']}")

        if categoria in ["ALTO", "CRITICO"]:
            print(f"Supervisión humana: {riesgo['supervision']}")


if __name__ == "__main__":
    evaluar_riesgos()