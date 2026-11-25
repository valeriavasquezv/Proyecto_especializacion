from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command


class EstadoDespliegue(TypedDict):
    huella_nueva: str
    aprobado: bool
    estado: str

def solicitar_aprobacion(estado: EstadoDespliegue):

    decision = interrupt({
        "mensaje": "¿Autorizar el despliegue de la nueva versión del prompt?",
        "huella_nueva": estado["huella_nueva"]
    })

    return {
        "aprobado": decision
    }


def aplicar_version(estado: EstadoDespliegue):

    if estado["aprobado"]:
        print("Nueva versión aprobada.")
        print("Huella activada:", estado["huella_nueva"])

        return {
            "estado": "APROBADO"
        }

    print("Despliegue rechazado.")
    print("Se conserva la versión anterior.")

    return {
        "estado": "RECHAZADO"
    }

def construir_grafo():

    flujo = StateGraph(EstadoDespliegue)

    # Registrar los nodos
    flujo.add_node("supervision", solicitar_aprobacion)
    flujo.add_node("aplicar", aplicar_version)

    # Definir el orden de ejecución
    flujo.add_edge(START, "supervision")
    flujo.add_edge("supervision", "aplicar")
    flujo.add_edge("aplicar", END)

    # Guardar el estado para poder pausar y reanudar
    memoria = InMemorySaver()

    # Compilar el grafo con checkpoint
    app_despliegue = flujo.compile(
        checkpointer=memoria
    )

    return app_despliegue

if __name__ == "__main__":

    app_despliegue = construir_grafo()

    # =================================
    # PRUEBA 1: APROBACIÓN
    # =================================

    print("\n=== PRUEBA DE APROBACIÓN ===")

    config1 = {
        "configurable": {
            "thread_id": "despliegue_aprobado"
        }
    }

    resultado1 = app_despliegue.invoke(
        {
            "huella_nueva": "abc123_version_1.1",
            "aprobado": False,
            "estado": "PENDIENTE"
        },
        config=config1
    )

    print("\nGrafo pausado:")
    print(resultado1)

    print("\nReanudando con aprobación humana...")

    resultado1 = app_despliegue.invoke(
        Command(resume=True),
        config=config1
    )

    print("\nResultado final:")
    print(resultado1)


    # =================================
    # PRUEBA 2: RECHAZO
    # =================================

    print("\n=== PRUEBA DE RECHAZO ===")

    config2 = {
        "configurable": {
            "thread_id": "despliegue_rechazado"
        }
    }

    resultado2 = app_despliegue.invoke(
        {
            "huella_nueva": "xyz789_version_1.1",
            "aprobado": False,
            "estado": "PENDIENTE"
        },
        config=config2
    )

    print("\nGrafo pausado:")
    print(resultado2)

    print("\nReanudando con rechazo humano...")

    resultado2 = app_despliegue.invoke(
        Command(resume=False),
        config=config2
    )

    print("\nResultado final:")
    print(resultado2)