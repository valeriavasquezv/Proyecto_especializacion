
import sys
import json
import time
from pathlib import Path

# Permite importar el módulo desde la carpeta src
RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ_PROYECTO))

from src.consumir_gemini import (
    armar_peticion,
    enviar_peticion,
    extraer_texto,
    parsear_respuesta_json
)

from prompts.banco import BANCO_DE_PROMPTS


def validar_respuesta(datos, claves_esperadas):
    """Comprueba que la respuesta sea un objeto con las claves requeridas."""
    if not isinstance(datos, dict):
        return False

    return all(clave in datos for clave in claves_esperadas)


def ejecutar_pruebas():
    registro = {}
    repeticiones = 3

    for prompt in BANCO_DE_PROMPTS:
        nombre = prompt["nombre"]
        exitos = 0
        fallos = []

        print(f"\nProbando prompt: {nombre}")

        for intento in range(1, repeticiones + 1):
            try:
                url, body = armar_peticion(
                    prompt["ejemplo_usuario"],
                    prompt["system_instruction"],
                    prompt.get("response_schema")
                )

                respuesta = enviar_peticion(url, body)
                texto = extraer_texto(respuesta)
                datos = parsear_respuesta_json(texto)

                if validar_respuesta(
                    datos,
                    prompt["claves_esperadas"]
                ):
                    exitos += 1
                    print(f"  Intento {intento}: correcto")
                else:
                    fallos.append({
                        "intento": intento,
                        "error": "Faltan claves esperadas en el JSON"
                    })
                    print(f"  Intento {intento}: estructura incorrecta")

            except (ValueError, RuntimeError, KeyError) as error:
                fallos.append({
                    "intento": intento,
                    "error": str(error)
                })
                print(f"  Intento {intento}: error - {error}")

            if intento < repeticiones:
                time.sleep(1)

        registro[nombre] = {
            "exitos": exitos,
            "fallos": len(fallos),
            "total_intentos": repeticiones,
            "detalle_fallos": fallos
        }

    ruta_registro = (
        Path(__file__).resolve().parent
        / "registro_resultados.json"
    )

    with open(ruta_registro, "w", encoding="utf-8") as archivo:
        json.dump(registro, archivo, ensure_ascii=False, indent=4)

    print("\nPruebas terminadas.")
    print(f"Registro guardado en: {ruta_registro}")

if __name__ == "__main__":
    ejecutar_pruebas()