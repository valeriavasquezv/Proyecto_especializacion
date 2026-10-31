import unittest
import sys
from pathlib import Path
from unittest.mock import patch

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ_PROYECTO))

from src.cliente import consultar_modelo
from src.cliente_reintento import con_reintento

class TestCliente(unittest.TestCase):

    @patch("src.cliente.extraer_texto")
    @patch("src.cliente.con_reintento")
    @patch("src.cliente.armar_peticion")
    def test_consultar_modelo(
        self,
        mock_armar,
        mock_reintento,
        mock_extraer,
    ):
        mock_armar.return_value = (
            "https://ejemplo.com",
            {"pregunta": "Hola"},
        )

        mock_reintento.return_value = {
        "respuesta": "simulada",
        "usageMetadata": {
        "promptTokenCount": 100,
        "candidatesTokenCount": 50,
        }
    }
        mock_extraer.return_value = "Hola, esta es una respuesta."

        resultado = consultar_modelo(
            "Hola",
            "Responde brevemente.",
        )

        self.assertEqual(
            resultado,
            "Hola, esta es una respuesta.",
        )

        mock_armar.assert_called_once()
        mock_reintento.assert_called_once()
        mock_extraer.assert_called_once()
    
    @patch("src.cliente.con_reintento")
    @patch("src.cliente.armar_peticion")
    def test_reintentos_agotados(
        self,
        mock_armar,
        mock_reintento,
    ):
        mock_armar.return_value = (
            "https://ejemplo.com",
            {"pregunta": "Hola"},
        )

        mock_reintento.side_effect = TimeoutError(
            "Proveedor no disponible"
        )

        with self.assertRaisesRegex(
            RuntimeError,
            "tras varios intentos",
        ):
            consultar_modelo("Hola")

        mock_reintento.assert_called_once()

    @patch("src.cliente_reintento.time.sleep")
    def test_reintenta_hasta_tener_exito(self, mock_sleep):
        operacion = unittest.mock.Mock(
            side_effect=[
                TimeoutError("Fallo temporal"),
                TimeoutError("Fallo temporal"),
                "Respuesta exitosa",
            ]
        )

        resultado = con_reintento(
            operacion,
            intentos=3,
            espera_base=2,
        )

        self.assertEqual(resultado, "Respuesta exitosa")
        self.assertEqual(operacion.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)

if __name__ == "__main__":
    unittest.main()
