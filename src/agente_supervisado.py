from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver

from src.agente_financiero import (
    calcular_indicadores_financieros,
    consultar_conceptos_financieros
)


def construir_agente_supervisado(modelo):

    herramientas = [
        calcular_indicadores_financieros,
        consultar_conceptos_financieros
    ]

    supervision = HumanInTheLoopMiddleware(
        interrupt_on={
            "calcular_indicadores_financieros": True
        }
    )

    agente = create_agent(
        model=modelo,
        tools=herramientas,
        system_prompt="""
        Eres PymeCopilot AI, un asistente especializado
        en gestión y análisis financiero empresarial.

        Utiliza las herramientas disponibles cuando
        necesites realizar cálculos financieros o
        consultar conceptos.

        No inventes cifras ni resultados financieros.
        Si faltan datos, solicita la información necesaria.
        Explica los resultados de manera clara y profesional.
        """,
        middleware=[supervision],
        checkpointer=InMemorySaver()
    )

    return agente
