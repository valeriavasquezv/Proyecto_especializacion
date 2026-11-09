
import re

def limpiar_texto(texto: str) -> str:
    """
    Normaliza un texto:
    - Convierte a minúsculas.
    - Elimina signos de puntuación.
    - Elimina espacios repetidos.
    """

    if not isinstance(texto, str):
        tipo = type(texto).__name__
        raise TypeError(f"limpiar_texto espera str, no {tipo}")

    texto = texto.lower()
    texto = re.sub(r"[^\w\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto

def tokenizar(texto_limpio: str) -> list[str]:
    """
    Divide un texto limpio en una lista de palabras.
    """
    return texto_limpio.split()
    
def procesar_texto(texto: str) -> list[str]:
    """
    Limpia un texto y luego lo divide en tokens.
    """
    texto_limpio = limpiar_texto(texto)
    tokens = tokenizar(texto_limpio)

    return tokens