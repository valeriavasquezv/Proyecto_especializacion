
import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()

def armar_peticion(
    pregunta_usuario,
    system_instruction,
    response_schema=None,
    modelo="gemini-3.1-flash-lite"
):
    if not pregunta_usuario:
        raise ValueError("La pregunta no puede estar vacía")

    api_key = os.getenv("GEMINI_API_KEY")

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/"
        f"models/{modelo}:generateContent?key={api_key}"
    )

    body = {
        "systemInstruction": {
            "parts": [{"text": system_instruction}]
        },
        "contents": [
            {"parts": [{"text": pregunta_usuario}]}
        ]
    }

    if response_schema is not None:
        body["generationConfig"] = {
            "responseMimeType": "application/json",
            "responseSchema": response_schema
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

def parsear_respuesta_json(texto):
    texto_limpio = texto.strip()
    texto_limpio = re.sub(r"^```(?:json)?\s*", "", texto_limpio)
    texto_limpio = re.sub(r"\s*```$", "", texto_limpio)

    try:
        datos = json.loads(texto_limpio)
    except json.JSONDecodeError:
        raise ValueError("La respuesta del modelo no es JSON válido.")

    if not isinstance(datos, dict):
        raise ValueError("La respuesta JSON debe ser un objeto.")

    return datos

def obtener_dato_de_prueba(pregunta):
    try:
        system_instruction = ("Eres un asistente técnico. Responde de forma breve y clara."
        )

        url, body = armar_peticion(
            pregunta,
            system_instruction
        )
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
    pregunta_usuario = (
        "Necesito ayuda para resetear mi contraseña, "
        "no me llega el correo de verificación."
    )

    system_instruction = (
        "Clasifica la solicitud del usuario. "
        "Responde únicamente con un objeto JSON válido."
    )

    response_schema = {
        "type": "OBJECT",
        "properties": {
            "categoria": {"type": "STRING"},
            "confianza": {"type": "NUMBER"}
        },
        "required": ["categoria", "confianza"]
    }

    url, body = armar_peticion(
        pregunta_usuario,
        system_instruction,
        response_schema
    )

    try:
        respuesta = enviar_peticion(url, body)
        texto = extraer_texto(respuesta)
        datos = parsear_respuesta_json(texto)

        print(datos)
        print(type(datos))

    except (RuntimeError, ValueError) as error:
        print("No se pudo completar la operación:", error)
                  