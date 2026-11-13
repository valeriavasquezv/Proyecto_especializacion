
from unittest.mock import MagicMock
from langchain_core.runnables import RunnableLambda
from src.enrutamiento import construir_cadena_con_enrutamiento
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda
from src.enrutamiento import construir_paso_clasificacion

def crear_clasificador(categoria):
    """Simula la clasificación sin llamar a Gemini."""
    return RunnableLambda(lambda entrada: categoria)


def crear_ruta(nombre):
    """Simula una ruta y permite identificar cuál se ejecutó."""
    return RunnableLambda(
        lambda entrada: f"Ruta ejecutada: {nombre}"
    )


def test_ruta_problema():

    cadena = construir_cadena_con_enrutamiento(
        paso_clasificacion=crear_clasificador("problema"),
        cadena_problema=crear_ruta("problema"),
        cadena_mejora=crear_ruta("mejora"),
        cadena_consulta=crear_ruta("consulta")
    )

    resultado = cadena.invoke({"mensaje": "No puedo pagar mis deudas"})

    assert resultado == "Ruta ejecutada: problema"


def test_ruta_mejora():

    cadena = construir_cadena_con_enrutamiento(
        paso_clasificacion=crear_clasificador("mejora"),
        cadena_problema=crear_ruta("problema"),
        cadena_mejora=crear_ruta("mejora"),
        cadena_consulta=crear_ruta("consulta")
    )

    resultado = cadena.invoke({"mensaje": "Quiero mejorar mis márgenes"})

    assert resultado == "Ruta ejecutada: mejora"


def test_ruta_por_defecto():

    cadena = construir_cadena_con_enrutamiento(
        paso_clasificacion=crear_clasificador("otra_categoria"),
        cadena_problema=crear_ruta("problema"),
        cadena_mejora=crear_ruta("mejora"),
        cadena_consulta=crear_ruta("consulta")
    )

    resultado = cadena.invoke({"mensaje": "Consulta general"})

    assert resultado == "Ruta ejecutada: consulta"

def test_normalizacion_clasificacion():

    # Simulamos una respuesta de Gemini con espacios y mayúsculas
    modelo_mock = RunnableLambda(
        lambda entrada: AIMessage(content="  PROBLEMA\n")
    )

    # Construimos el clasificador real
    clasificador = construir_paso_clasificacion(modelo_mock)

    # Ejecutamos la clasificación
    resultado = clasificador.invoke({
        "mensaje": "Tengo problemas para pagar mis obligaciones"
    })

    # Verificamos la normalización
    assert resultado == "problema"
