import unittest
import sys
from pathlib import Path
from unittest.mock import patch

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ_PROYECTO))

import src.cliente as cliente
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
    
    def test_registrar_costo_acumula(self):
        # Reiniciamos el acumulador
        cliente.costo_total_sesion = 0.0

        # Simulamos una respuesta de Gemini
        respuesta_falsa = {
            "usageMetadata": {
                "promptTokenCount": 1000,
                "candidatesTokenCount": 500,
            }
        }

        costo = cliente.registrar_costo(respuesta_falsa)

        # Calculamos el resultado esperado
        costo_esperado = (
            1000 * cliente.PRECIO_ENTRADA
            + 500 * cliente.PRECIO_SALIDA
        )

        self.assertAlmostEqual(costo, costo_esperado)
        self.assertAlmostEqual(
            cliente.costo_total_sesion,
            costo_esperado,
        )

    @patch("src.cliente_reintento.time.sleep")
    def test_no_reintenta_value_error(self, mock_sleep):
        operacion = unittest.mock.Mock(
            side_effect=ValueError("Error de validación")
        )

        with self.assertRaises(ValueError):
            con_reintento(
                operacion,
                intentos=3,
                espera_base=2,
            )

        self.assertEqual(operacion.call_count, 1)
        mock_sleep.assert_not_called()

    @patch("src.cliente_reintento.time.sleep")
    def test_agota_intentos_y_propaga_timeout(self, mock_sleep):
        operacion = unittest.mock.Mock(
            side_effect=TimeoutError("Proveedor no disponible")
        )

        with self.assertRaises(TimeoutError):
            con_reintento(
                operacion,
                intentos=3,
                espera_base=2,
            )

        self.assertEqual(operacion.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)

    @patch("src.cliente.armar_peticion")
    def test_consultar_modelo_propaga_value_error(self, mock_armar):
        mock_armar.side_effect = ValueError("Credencial inválida")

        with self.assertRaisesRegex(ValueError, "Credencial inválida"):
            consultar_modelo("Hola")

        mock_armar.assert_called_once()

if __name__ == "__main__":
    unittest.main()
