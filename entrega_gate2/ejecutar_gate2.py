
import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

PRUEBAS = [
    ("Recuperación RAG", ROOT / "Demos" / "prueba_recuperacion.py"),
    ("Evaluación RAG", ROOT / "Demos" / "evaluacion_consultas_rag.py"),
    ("Privacidad y trazabilidad", ROOT / "Demos" / "prueba_trazabilidad.py"),
    ("Supervisión humana", ROOT / "entrega_gate2" / "prueba_supervision.py"),
]

def main():
    print("\n=== EJECUCIÓN DE PRUEBAS GATE 2 ===")

    if not os.getenv("GEMINI_API_KEY"):
        print("[ERROR] Falta GEMINI_API_KEY.")
        return 1

    if not (ROOT / "vectorstore").exists():
        print("[ERROR] No existe la carpeta vectorstore.")
        return 1

    resultados = []

    for nombre, archivo in PRUEBAS:
        print(f"\n--- {nombre} ---")

        if not archivo.exists():
            print(f"[ERROR] No existe {archivo}")
            resultados.append((nombre, "NO EJECUTADA"))
            continue

        proceso = subprocess.run(
            [sys.executable, str(archivo)],
            cwd=ROOT
        )

        estado = "OK" if proceso.returncode == 0 else "ERROR"
        resultados.append((nombre, estado))

        if estado == "ERROR":
            break

    print("\n=== RESUMEN ===")
    for nombre, estado in resultados:
        print(f"{estado} | {nombre}")

    return 0 if len(resultados) == len(PRUEBAS) and all(
        estado == "OK" for _, estado in resultados
    ) else 1


if __name__ == "__main__":
    sys.exit(main())
