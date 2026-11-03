
import unittest
from unittest.mock import Mock, patch

from src.consumir_gemini import enviar_peticion


class TestErroresAPI(unittest.TestCase):

    @patch("src.consumir_gemini.requests.post")
    def test_error_autenticacion_401(self, mock_post):
        respuesta = Mock()
        respuesta.status_code = 401
        mock_post.return_value = respuesta

        with self.assertRaisesRegex(ValueError, "Credencial inválida"):
            enviar_peticion("https://ejemplo.com", {})

    @patch("src.consumir_gemini.requests.post")
    def test_limite_solicitudes_429(self, mock_post):
        respuesta = Mock()
        respuesta.status_code = 429
        mock_post.return_value = respuesta

        with self.assertRaises(TimeoutError):
            enviar_peticion("https://ejemplo.com", {})

    @patch("src.consumir_gemini.requests.post")
    def test_error_temporal_503(self, mock_post):
        respuesta = Mock()
        respuesta.status_code = 503
        mock_post.return_value = respuesta

        with self.assertRaises(TimeoutError):
            enviar_peticion("https://ejemplo.com", {})

    @patch("src.consumir_gemini.requests.post")
    def test_respuesta_exitosa(self, mock_post):
        respuesta = Mock()
        respuesta.status_code = 200
        respuesta.json.return_value = {"texto": "Respuesta simulada"}
        mock_post.return_value = respuesta

        resultado = enviar_peticion("https://ejemplo.com", {})

        self.assertEqual(resultado, {"texto": "Respuesta simulada"})


if __name__ == "__main__":
    unittest.main()
