from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain_classic.agents import (
    AgentExecutor,
    create_tool_calling_agent
)
from langchain_core.chat_history import (
    InMemoryChatMessageHistory
)
from langchain_core.runnables.history import (
    RunnableWithMessageHistory
)

class ArgumentosIndicadoresFinancieros(BaseModel):

    ingresos: float = Field(
        description=(
            "Ingresos totales de la empresa "
            "en el período analizado."
        )
    )

    costos: float = Field(
        description=(
            "Costos asociados a la producción "
            "o prestación de servicios."
        )
    )

    gastos: float = Field(
        description=(
            "Gastos operacionales y administrativos "
            "de la empresa."
        )
    )


@tool(
    "calcular_indicadores_financieros",
    args_schema=ArgumentosIndicadoresFinancieros
)
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
    ("system", """
        Eres PymeCopilot AI, un asistente especializado
        en gestión y análisis financiero empresarial.

        Utiliza las herramientas disponibles cuando
        necesites realizar cálculos financieros o
        consultar conceptos.

        Puedes utilizar más de una herramienta si
        la solicitud lo requiere.

        No inventes cifras ni resultados financieros.
        Si faltan datos, solicita la información necesaria.
        Explica los resultados de manera clara y profesional.
    """),
    MessagesPlaceholder("chat_history"),
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

# Historial independiente por sesión
historiales = {}

def obtener_historial(session_id: str):
    if session_id not in historiales:
        historiales[session_id] = InMemoryChatMessageHistory()

    return historiales[session_id]

def construir_agente_con_memoria(modelo):
    ejecutor = construir_agente(modelo)

    def ejecutar_y_normalizar(entrada):
        resultado = ejecutor.invoke(entrada)

        salida = resultado.get("output", "")

        # Normalizar respuestas estructuradas de Gemini
        if isinstance(salida, list):
            salida = "".join(
                bloque.get("text", "")
                for bloque in salida
                if isinstance(bloque, dict)
                and bloque.get("type") == "text"
            )

        resultado["output"] = salida

        return resultado

    ejecutor_normalizado = RunnableLambda(
        ejecutar_y_normalizar
    )

    agente_con_memoria = RunnableWithMessageHistory(
        ejecutor_normalizado,
        obtener_historial,
        input_messages_key="entrada",
        history_messages_key="chat_history",
        output_messages_key="output"
    )

    return agente_con_memoria
