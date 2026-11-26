
import json
from datetime import datetime, timezone
from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver


class EstadoSupervision(TypedDict):
    session_id: str
    accion: str
    aprobacion: bool
    estado: str


def solicitar_aprobacion(state: EstadoSupervision):

    decision = interrupt({
        "mensaje": "Se requiere aprobación humana.",
        "accion": state["accion"],
        "session_id": state["session_id"]
    })

    return {
        "aprobacion": bool(decision),
        "estado": "aprobado" if decision else "rechazado"
    }


def registrar_aprobacion(state: EstadoSupervision):

    registro = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": state["session_id"],
        "evento": "supervision_humana",
        "aprobacion": state["aprobacion"],
        "estado": state["estado"]
    }

    with open(
        "trazas_supervision.jsonl",
        "a",
        encoding="utf-8"
    ) as archivo:

        archivo.write(
            json.dumps(registro, ensure_ascii=False) + "\n"
        )

    return {}


def construir_flujo_supervision():

    grafo = StateGraph(EstadoSupervision)

    grafo.add_node(
        "solicitar_aprobacion",
        solicitar_aprobacion
    )

    grafo.add_node(
        "registrar_aprobacion",
        registrar_aprobacion
    )

    grafo.add_edge(START, "solicitar_aprobacion")

    grafo.add_edge(
        "solicitar_aprobacion",
        "registrar_aprobacion"
    )

    grafo.add_edge("registrar_aprobacion", END)

    memoria = MemorySaver()

    return grafo.compile(checkpointer=memoria)


if __name__ == "__main__":

    flujo = construir_flujo_supervision()

    configuracion = {
        "configurable": {
            "thread_id": "prueba_gate2_001"
        }
    }

    estado_inicial = {
        "session_id": "prueba_gate2_001",
        "accion": "Ejecutar una operación financiera sensible.",
        "aprobacion": False,
        "estado": "pendiente"
    }

    print("\nSOLICITANDO APROBACIÓN HUMANA...")

    resultado = flujo.invoke(
        estado_inicial,
        config=configuracion
    )

    print("\nRESULTADO DE LA INTERRUPCIÓN:")
    print(resultado)

    if resultado.get("__interrupt__"):

        decision = input(
            "\n¿Apruebas la operación? (s/n): "
        ).strip().lower()

        aprobada = decision == "s"

        print("\nREANUDANDO FLUJO...")

        resultado_final = flujo.invoke(
            Command(resume=aprobada),
            config=configuracion
        )

        print("\nRESULTADO FINAL:")
        print(resultado_final)
