
import json
from datetime import datetime, timezone


def registrar_traza(
    session_id: str,
    entrada: str,
    resultado: dict
) -> None:
    """
    Guarda una interacción del agente en un archivo JSONL.
    Registra la entrada, las herramientas utilizadas
    y la respuesta final.
    """

    registro = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "entrada": entrada,
        "acciones": [
            {
                "herramienta": accion.tool,
                "argumentos": accion.tool_input,
                "observacion": observacion
            }
            for accion, observacion
            in resultado.get("intermediate_steps", [])
        ],
        "respuesta_final": resultado["output"]
    }

    with open(
        "trazas_agente.jsonl",
        "a",
        encoding="utf-8"
    ) as archivo:

        archivo.write(
            json.dumps(registro, ensure_ascii=False) + "\n"
        )


def marcar_repeticiones_sospechosas(
    archivo: str = "trazas_agente.jsonl"
) -> None:
    """
    Detecta si una misma herramienta fue invocada
    varias veces consecutivas dentro de una interacción.
    """

    try:
        with open(archivo, encoding="utf-8") as f:
            registros = [
                json.loads(linea)
                for linea in f
                if linea.strip()
            ]

    except FileNotFoundError:
        print(f"No se encontró el archivo: {archivo}")
        return

    for registro in registros:

        herramientas = [
            accion["herramienta"]
            for accion in registro.get("acciones", [])
        ]

        for i in range(1, len(herramientas)):

            if herramientas[i] == herramientas[i - 1]:

                print(
                    f"Revisar sesión {registro['session_id']}: "
                    f"la herramienta '{herramientas[i]}' "
                    "se utilizó dos veces seguidas."
                )
                break
