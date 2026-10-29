
from src.consumir_gemini import (
    armar_peticion,
    enviar_peticion,
    extraer_texto,
)
from src.cliente_reintento import con_reintento


def consultar_modelo(
    pregunta: str,
    system_instruction: str = "",
    response_schema=None,
) -> str:
    """
    Consulta el modelo de IA y devuelve el texto generado.

    Reintenta automáticamente ante errores temporales.
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

    return extraer_texto(respuesta)