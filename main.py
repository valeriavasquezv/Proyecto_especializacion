
import json

from src.consumir_gemini import (
    armar_peticion,
    enviar_peticion,
    extraer_texto,
    parsear_respuesta_json,
)
from prompts.banco import BANCO_DE_PROMPTS


def main():
    pregunta_usuario = (
        "Quiero preparar brownies. "
        "Tengo 250 g de chocolate que cuestan $2000 "
        "y 100 g de mantequilla que cuestan $1000. "
        "Organiza los datos de la receta."
    )

    prompt = next(
    p for p in BANCO_DE_PROMPTS
    if p["nombre"] == "estructurar_receta"
)

    system_instruction = prompt["system_instruction"]
    response_schema = prompt["response_schema"]

    try:
        url, body = armar_peticion(
            pregunta_usuario,
            system_instruction,
            response_schema,
        )

        respuesta = enviar_peticion(url, body)
        texto = extraer_texto(respuesta)
        datos = parsear_respuesta_json(texto)

        print("\nResultado de la miniaplicación:")
        print(json.dumps(datos, ensure_ascii=False, indent=2))

    except (RuntimeError, ValueError, KeyError) as error:
        print(f"\nNo se pudo completar la operación: {error}")


if __name__ == "__main__":
    main()
