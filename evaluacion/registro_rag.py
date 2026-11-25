
import time
import json
from datetime import datetime, timezone
from pathlib import Path

# Archivo donde se almacenará el historial de ejecuciones
ARCHIVO_REGISTRO = Path("evaluacion/registros_latencia_costo.jsonl")


def medir_tiempo(funcion, *args, **kwargs):
    """
    Ejecuta una función y mide cuánto tarda.

    Retorna:
    - resultado de la función
    - tiempo transcurrido en segundos
    """
    inicio = time.perf_counter()

    resultado = funcion(*args, **kwargs)

    fin = time.perf_counter()
    tiempo_transcurrido = fin - inicio

    return resultado, tiempo_transcurrido


def guardar_registro(registro):
    """
    Guarda una ejecución del flujo RAG en formato JSONL.
    Cada ejecución ocupa una línea independiente.
    """
    ARCHIVO_REGISTRO.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with ARCHIVO_REGISTRO.open("a", encoding="utf-8") as archivo:
        archivo.write(
            json.dumps(registro, ensure_ascii=False) + "\n"
        )

from src.cliente import PRECIO_ENTRADA, PRECIO_SALIDA
from src.consumir_gemini import calcular_costo
from src.cliente_reintento import con_reintento

def obtener_metricas_tokens(respuesta_api):
    """
    Extrae los tokens utilizados por Gemini
    y calcula el costo de generación.
    """
    uso = respuesta_api.get("usageMetadata", {})

    tokens_entrada = uso.get("promptTokenCount", 0)
    tokens_salida = uso.get("candidatesTokenCount", 0)

    total_tokens = tokens_entrada + tokens_salida

    costo = calcular_costo(
        respuesta_api,
        PRECIO_ENTRADA,
        PRECIO_SALIDA
    )

    return {
        "tokens_entrada": tokens_entrada,
        "tokens_salida": tokens_salida,
        "total_tokens": total_tokens,
        "costo_usd": costo
    }

from src.recuperacion_rag import construir_prompt
from src.consumir_gemini import (
    armar_peticion,
    enviar_peticion,
    extraer_texto
)


def ejecutar_rag_medido(pregunta, k=3):

    inicio_total = time.perf_counter()

    # 1. Recuperación de documentos y construcción del prompt
    resultado_prompt, tiempo_recuperacion = medir_tiempo(
        construir_prompt,
        pregunta,
        k
    )

    prompt, citas = resultado_prompt

    # 2. Preparación de la petición
    system_instruction = (
        "Eres un asistente financiero. "
        "Responde utilizando exclusivamente el contexto "
        "proporcionado y cita las fuentes con [1], [2], etc. "
        "Si la información no es suficiente, indícalo."
    )

    url, body = armar_peticion(
        pregunta_usuario=prompt,
        system_instruction=system_instruction
    )

    # 3. Generación de respuesta y medición de latencia
    respuesta_api, tiempo_generacion = medir_tiempo(
        lambda: con_reintento(
            lambda: enviar_peticion(url, body)
    )
)
    respuesta = extraer_texto(respuesta_api)

    fin_total = time.perf_counter()
    tiempo_total = fin_total - inicio_total

    # 4. Extracción de tokens y cálculo de costo
    metricas_tokens = obtener_metricas_tokens(respuesta_api)

    # 5. Construcción del registro
    registro = {
        "fecha": datetime.now(timezone.utc).isoformat(),
        "pregunta": pregunta,
        "k": k,
        "latencia_recuperacion_seg": tiempo_recuperacion,
        "latencia_generacion_seg": tiempo_generacion,
        "latencia_total_seg": tiempo_total,
        **metricas_tokens
    }

    # 6. Almacenamiento histórico
    guardar_registro(registro)

    return respuesta, citas, registro
