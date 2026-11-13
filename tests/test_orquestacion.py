
from unittest.mock import MagicMock

from langchain_core.runnables import RunnableLambda

from src.enrutamiento import (
    construir_cadena_problema_segura,
    construir_cadena_con_enrutamiento,
    procesar_mensaje_seguro
)


def test_fallback_ante_fallo_de_ruta():

    def fallar_a_proposito(entrada):
        raise ConnectionError("Error simulado")

    cadena_falsa = RunnableLambda(fallar_a_proposito)

    cadena_segura = construir_cadena_problema_segura(
        cadena_falsa
    )

    resultado = cadena_segura.invoke(
        {"mensaje": "Tengo problemas financieros"}
    )

    assert "revisar" in resultado.lower()


def test_procesar_mensaje_seguro_no_propaga_excepciones():

    clasificacion_falsa = MagicMock()
    clasificacion_falsa.side_effect = ConnectionError(
        "Error de clasificación simulado"
    )

    cadena_falsa = construir_cadena_con_enrutamiento(
        paso_clasificacion=clasificacion_falsa
    )

    resultado = procesar_mensaje_seguro(
        cadena_falsa,
        "Tengo problemas para pagar mis obligaciones"
    )

    assert "no pudimos procesar" in resultado.lower()
