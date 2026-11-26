import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from langgraph.types import Command
from src.supervision_humana import construir_flujo_supervision

ARCHIVO_TRAZAS = ROOT / "trazas_supervision.jsonl"

def main():
    flujo = construir_flujo_supervision()

    config = {
        "configurable": {
            "thread_id": "prueba_gate2_supervision"
        }
    }

    estado_inicial = {
        "session_id": "prueba_gate2_supervision",
        "accion": "Ejecutar una operación financiera",
        "aprobacion": False,
        "estado": "pendiente"
    }

    resultado = flujo.invoke(estado_inicial, config=config)

    interrupciones = resultado.get("__interrupt__", [])

    assert interrupciones, "El flujo no se interrumpió solicitando aprobación."

    print("[OK] El flujo se interrumpió esperando aprobación humana.")

    resultado_final = flujo.invoke(
        Command(resume=True),
        config=config
    )

    assert resultado_final["aprobacion"] is True
    assert resultado_final["estado"] == "aprobado"

    print("[OK] El flujo se reanudó con aprobación humana.")

    registros = [
        json.loads(line)
        for line in ARCHIVO_TRAZAS.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    registro = next(
        (
            r for r in reversed(registros)
            if r.get("session_id") == "prueba_gate2_supervision"
        ),
        None
    )

    assert registro is not None, "No se encontró el registro de auditoría."
    assert registro["aprobacion"] is True
    assert registro["estado"] == "aprobado"

    print("[OK] La aprobación quedó registrada en auditoría.")
    print("\n[OK] Prueba de supervisión humana superada.")

if __name__ == "__main__":
    main()