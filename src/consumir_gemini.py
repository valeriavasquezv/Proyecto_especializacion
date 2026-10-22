
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def armar_peticion(
    pregunta,
    modelo="gemini-3.1-flash-lite"
):
    if not pregunta:
        raise ValueError("La pregunta no puede estar vacía")

    api_key = os.getenv("GEMINI_API_KEY")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}"

    body = {
        "contents": [
            {"parts": [{"text": pregunta}]}
        ]
    }

    return url, body

def enviar_peticion(url, body):
    try:
        respuesta = requests.post(url, json=body)
        respuesta.raise_for_status()

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "No se pudo conectar con el servicio. "
            "Intenta de nuevo en unos segundos."
        )

    except requests.exceptions.HTTPError as error:
        if respuesta.status_code == 503:
            raise RuntimeError(
                f"Gemini respondió con HTTP 503. "
                f"Detalle: {respuesta.text}"
            )
        raise RuntimeError(
            f"El servicio respondió con un error HTTP: {error}. "
            f"Detalle: {respuesta.text}"
        )

    try:
        return respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError(
            "La respuesta del servicio no llegó en el formato esperado."
        )

def extraer_texto(datos):
    try:
        return datos["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise RuntimeError(
            "La respuesta no trae el texto generado en el lugar esperado."
        )

def obtener_dato_de_prueba(pregunta):
    try:
        url, body = armar_peticion(pregunta)
        datos = enviar_peticion(url, body)
        
        texto = extraer_texto(datos)
        return texto
    
    except (ValueError, RuntimeError) as error:
        print("No se pudo completar la operación:", error)

def calcular_costo(datos, precio_entrada, precio_salida):
    uso = datos["usageMetadata"]

    tokens_entrada = uso["promptTokenCount"]
    tokens_salida = uso["candidatesTokenCount"]

    return (
        tokens_entrada * precio_entrada
        + tokens_salida * precio_salida
    )

if __name__ == "__main__":
    print(obtener_dato_de_prueba(
        "Confirma en una frase corta que esta conexión funciona"
    ))                      