import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.types import Command
from langchain_core.messages import ToolMessage

from src.agente_supervisado import construir_agente_supervisado

ARCHIVO_TRAZAS = ROOT / "entrega_gate2" / "resultados" / "trazas_supervision.jsonl"


def registrar_evidencia(session_id, decision, estado):
    registro = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "evento": "supervision_humana",
        "herramienta": "calcular_indicadores_financieros",
        "decision": decision,
        "estado": estado
    }

    with ARCHIVO_TRAZAS.open("a", encoding="utf-8") as archivo:
        archivo.write(json.dumps(registro, ensure_ascii=False) + "\n")


def ejecutar_prueba(agente, decision):
    session_id = f"gate2_{decision}"

    config = {
        "configurable": {
            "thread_id": session_id
        }
    }

    resultado = agente.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Calcula mis indicadores financieros: "
                        "ingresos 10000000, costos 5000000 "
                        "y gastos 2000000."
                    )
                }
            ]
        },
        config=config
    )

    interrupciones = resultado.get("__interrupt__", [])
    assert interrupciones, "El agente no solicitó aprobación humana."

    print(f"[OK] Supervisión activada para {decision}.")

    respuesta = agente.invoke(
        Command(
            resume={
                "decisions": [
                    {
                        "type": "approve" if decision == "aprobacion" else "reject",
                        **(
                            {}
                            if decision == "aprobacion"
                            else {"message": "Operación rechazada por el revisor humano."}
                        )
                    }
                ]
            }
        ),
        config=config
    )

    mensajes = respuesta.get("messages", [])

    calculo_ejecutado = any(
        isinstance(mensaje, ToolMessage)
        and mensaje.name == "calcular_indicadores_financieros"
        and "Resultados financieros:" in str(mensaje.content)
        for mensaje in mensajes
    )

    if decision == "aprobacion":
        assert calculo_ejecutado, "El cálculo no se ejecutó después de aprobar."
        estado = "aprobado"
        print("[OK] El cálculo se ejecutó tras la aprobación.")

    else:
        assert not calculo_ejecutado, "El cálculo se ejecutó pese al rechazo."
        estado = "rechazado"
        print("[OK] El cálculo no se ejecutó tras el rechazo.")

    registrar_evidencia(session_id, decision, estado)


def main():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("No se encontró GEMINI_API_KEY.")

    modelo = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        google_api_key=api_key,
        temperature=0
    )

    agente = construir_agente_supervisado(modelo)

    ejecutar_prueba(agente, "aprobacion")
    ejecutar_prueba(agente, "rechazo")

    print("\n[OK] Pruebas de supervisión humana completadas.")
    print(f"[OK] Evidencias guardadas en: {ARCHIVO_TRAZAS}")


if __name__ == "__main__":
    main()
