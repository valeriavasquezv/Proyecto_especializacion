from langchain_core.tools import tool
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain_classic.agents import (
    AgentExecutor,
    create_tool_calling_agent
)

@tool
def calcular_indicadores_financieros(
    ingresos: float,
    costos: float,
    gastos: float
) -> str:
    """
    Calcula indicadores financieros de una empresa,
    incluyendo utilidad, margen de utilidad y porcentaje
    de costos y gastos. Usar cuando el usuario proporcione
    cifras financieras y solicite evaluar su rentabilidad.
    """

    if ingresos <= 0:
        return "Error: los ingresos deben ser mayores que cero."

    utilidad = ingresos - costos - gastos
    margen = (utilidad / ingresos) * 100
    porcentaje_costos = (costos / ingresos) * 100
    porcentaje_gastos = (gastos / ingresos) * 100

    return (
        f"Resultados financieros:\n"
        f"Ingresos: ${ingresos:,.2f}\n"
        f"Costos: ${costos:,.2f}\n"
        f"Gastos: ${gastos:,.2f}\n"
        f"Utilidad: ${utilidad:,.2f}\n"
        f"Margen de utilidad: {margen:.2f}%\n"
        f"Costos sobre ingresos: {porcentaje_costos:.2f}%\n"
        f"Gastos sobre ingresos: {porcentaje_gastos:.2f}%"
    )

@tool
def consultar_conceptos_financieros(
    concepto: str
) -> str:
    """
    Consulta definiciones y explicaciones específicas
    de conceptos financieros como liquidez, EBITDA,
    capital de trabajo, punto de equilibrio y margen
    de utilidad.

    Usar exclusivamente cuando el usuario pregunte
    por uno de estos conceptos específicos.

    No utilizar para preguntas generales sobre gestión
    financiera, administración, estrategias o consejos
    empresariales que puedan responderse directamente.
    """

    conceptos = {
        "liquidez": (
            "La liquidez representa la capacidad de una "
            "empresa para cumplir sus obligaciones de corto plazo."
        ),
        "ebitda": (
            "El EBITDA mide el resultado operativo antes de "
            "intereses, impuestos, depreciaciones y amortizaciones."
        ),
        "capital de trabajo": (
            "El capital de trabajo corresponde a los activos "
            "corrientes menos los pasivos corrientes."
        ),
        "punto de equilibrio": (
            "Es el nivel de ventas en que los ingresos totales "
            "igualan los costos y gastos totales."
        ),
        "margen de utilidad": (
            "Es el porcentaje de los ingresos que permanece "
            "como utilidad después de descontar costos y gastos."
        )
    }

    concepto = concepto.strip().lower()

    for clave, definicion in conceptos.items():
        if clave in concepto:
            return definicion

    return (
        f"No se encontró información sobre '{concepto}'. "
        "Puedes consultar liquidez, EBITDA, capital de trabajo, "
        "punto de equilibrio o margen de utilidad."
    )

def construir_agente(modelo):

    herramientas = [
        calcular_indicadores_financieros,
        consultar_conceptos_financieros
    ]

    prompt_agente = ChatPromptTemplate.from_messages([
        (
            
            """
            Eres PymeCopilot AI, un asistente especializado
            en gestión y análisis financiero empresarial.

            Dispones de herramientas para realizar cálculos
            y consultar conceptos financieros específicos.

            Decide cuándo necesitas utilizar una herramienta.

            Utiliza las herramientas cuando necesites realizar
            cálculos o consultar conceptos financieros específicos.

            Para preguntas generales, explicaciones o consejos
            empresariales, responde directamente sin utilizar
            herramientas.

            Puedes utilizar varias herramientas si la solicitud
            lo requiere.

            No inventes cifras ni resultados financieros.
            Si faltan datos para realizar un cálculo, solicita
            la información necesaria.

            Explica los resultados de manera clara y profesional.
            """

        ),
        ("human", "{entrada}"),
        MessagesPlaceholder("agent_scratchpad")
    ])

    agente = create_tool_calling_agent(
        modelo,
        herramientas,
        prompt_agente
    )

    ejecutor_agente = AgentExecutor(
        agent=agente,
        tools=herramientas,
        verbose=True,
        return_intermediate_steps=True,
        max_iterations=5
    )

    return ejecutor_agente
