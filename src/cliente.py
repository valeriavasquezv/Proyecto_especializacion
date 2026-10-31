from src.consumir_gemini import (
    armar_peticion,
    enviar_peticion,
    extraer_texto,
    calcular_costo,
)
from src.cliente_reintento import con_reintento

# Precios del modelo elegido: gemini-3.1-flash-lite
PRECIO_ENTRADA = 0.25 / 1_000_000
PRECIO_SALIDA = 1.50 / 1_000_000

# Acumulador de costos de la sesión
costo_total_sesion = 0.0

def registrar_costo(respuesta: dict) -> float:
    global costo_total_sesion

    costo = calcular_costo(
        respuesta,
        PRECIO_ENTRADA,
        PRECIO_SALIDA,
    )

    costo_total_sesion += costo

    uso = respuesta["usageMetadata"]
    total_tokens = (
        uso["promptTokenCount"]
        + uso["candidatesTokenCount"]
    )

    print(
        f"Operación: {total_tokens} tokens, "
        f"costo estimado: US$ {costo:.8f} "
        f"(acumulado: US$ {costo_total_sesion:.8f})"
    )

    return costo

def consultar_modelo(
    pregunta: str,
    system_instruction: str = "",
    response_schema=None,
) -> str:
    """
    Consulta el modelo de IA y devuelve el texto generado.

    Reintenta automáticamente ante errores temporales
    y registra el costo de cada operación exitosa.
    """
    url, body = armar_peticion(
        pregunta,
        system_instruction,
        response_schema,
    )

    try:
        respuesta = con_reintento(
            lambda: enviar_peticion(url, body)
        )
    except TimeoutError as error:
        raise RuntimeError(
            "El servicio no respondió tras varios intentos. "
            "Intenta más tarde."
        ) from error

    registrar_costo(respuesta)

    return extraer_texto(respuesta)

