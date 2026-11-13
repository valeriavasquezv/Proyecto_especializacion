
from unittest.mock import MagicMock

from langchain_core.messages import AIMessage

from src.cadena_tres_pasos import construir_cadena


def test_cadena_tres_pasos():

    # Simulamos las tres respuestas de Gemini
    modelo_mock = MagicMock()

    modelo_mock.side_effect = [
        AIMessage(content="Análisis: la empresa tiene costos elevados."),
        AIMessage(content="Diagnóstico: existe una baja rentabilidad."),
        AIMessage(content="Recomendaciones: reducir costos y optimizar gastos.")
    ]

    # Construimos la cadena
    cadena = construir_cadena(modelo_mock)

    # Datos de entrada
    datos = {
        "tipo_negocio": "empresa de transporte",
        "ingresos": 8000000,
        "costos": 5000000,
        "gastos": 1500000
    }

    # Ejecutamos la cadena
    resultado = cadena.invoke(datos)

    # Verificamos el resultado final
    assert resultado == (
        "Recomendaciones: reducir costos y optimizar gastos."
    )

    # Verificamos las tres llamadas
    assert modelo_mock.call_count == 3
