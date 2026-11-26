
from types import SimpleNamespace
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.trazabilidad import registrar_traza

archivo = "trazas_prueba.jsonl"

resultado_simulado = {
    "intermediate_steps": [
        (
            SimpleNamespace(
                tool="calcular_indicadores_financieros",
                tool_input={
                    "ingresos": 10000000,
                    "costos": 5000000,
                    "gastos": 2000000
                }
            ),
            "Utilidad: 3000000"
        )
    ],
    "output": "La utilidad es de 3000000."
}

# Redirigir temporalmente el archivo de prueba
import builtins

open_original = builtins.open

def abrir_archivo(ruta, *args, **kwargs):
    if ruta == "trazas_agente.jsonl":
        ruta = archivo
    return open_original(ruta, *args, **kwargs)

builtins.open = abrir_archivo

try:
    registrar_traza(
        session_id="empresa_prueba",
        entrada="Consulta financiera simulada",
        resultado=resultado_simulado
    )
finally:
    builtins.open = open_original

with open(archivo, encoding="utf-8") as f:
    registro = json.loads(f.readline())

print("REGISTRO GENERADO:")
print(json.dumps(registro, indent=4, ensure_ascii=False))

assert "entrada" not in registro
assert "respuesta_final" not in registro
assert "argumentos" not in registro
assert "observacion" not in registro
assert registro["cantidad_herramientas"] == 1
assert registro["herramientas"] == [
    "calcular_indicadores_financieros"
]

print("\n[OK] La prueba de privacidad y trazabilidad fue superada.")

os.remove(archivo)
