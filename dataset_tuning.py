import json
from collections import Counter
from google.genai import types


# ==========================================
# PASO 1: DATASET PROPIO DE PYME COPILOT AI
# ==========================================

# Clasificar mensajes financieros de PYMEs
# según su intención y nivel de prioridad.

ejemplos_raw = [

    (
        "No tengo dinero suficiente para pagar "
        "a mis proveedores esta semana.",
        {
            "intencion": "flujo_caja",
            "prioridad": "alta"
        }
    ),

    (
        "Quiero saber cuánto dinero entra y sale "
        "de mi negocio cada mes.",
        {
            "intencion": "flujo_caja",
            "prioridad": "baja"
        }
    ),

    (
        "Mis costos aumentaron mucho este mes "
        "y estoy perdiendo margen.",
        {
            "intencion": "costos",
            "prioridad": "alta"
        }
    ),

    (
        "Necesito revisar cuánto me cuesta "
        "producir cada uno de mis productos.",
        {
            "intencion": "costos",
            "prioridad": "media"
        }
    ),

    (
        "Las ventas de esta semana cayeron "
        "considerablemente.",
        {
            "intencion": "ventas",
            "prioridad": "alta"
        }
    ),

    (
        "Quiero comparar las ventas de este mes "
        "con las del mes anterior.",
        {
            "intencion": "ventas",
            "prioridad": "baja"
        }
    ),

    (
        "No sé si mi negocio está generando "
        "ganancias o pérdidas.",
        {
            "intencion": "rentabilidad",
            "prioridad": "media"
        }
    ),

    (
        "Estoy vendiendo por debajo de mis costos "
        "y necesito revisar mi rentabilidad.",
        {
            "intencion": "rentabilidad",
            "prioridad": "alta"
        }
    ),

    (
        "Quiero organizar un presupuesto "
        "para el próximo trimestre.",
        {
            "intencion": "presupuesto",
            "prioridad": "media"
        }
    ),

    (
        "Necesito estimar cuánto dinero puedo "
        "destinar a gastos el próximo mes.",
        {
            "intencion": "presupuesto",
            "prioridad": "baja"
        }
    ),

    (
        "Tengo varias facturas vencidas "
        "y no puedo cubrir mis deudas.",
        {
            "intencion": "deudas",
            "prioridad": "alta"
        }
    ),

    (
        "Quiero conocer cuánto debo actualmente "
        "y ordenar mis compromisos de pago.",
        {
            "intencion": "deudas",
            "prioridad": "media"
        }
    ),
]

def chequear_balance(ejemplos_raw, clave):
    conteo = Counter(
        salida[clave]
        for texto, salida in ejemplos_raw
    )

    return conteo

def validar_dataset(
    examples: list[types.TuningExample],
    claves_esperadas: tuple[str, ...]
) -> list[str]:

    problemas = []
    vistos = set()

    for i, ej in enumerate(examples):

        if not ej.text_input or not ej.text_input.strip():
            problemas.append(f"ejemplo {i}: text_input vacio")

        if not ej.output or not ej.output.strip():
            problemas.append(f"ejemplo {i}: output vacio")
            continue

        if ej.text_input in vistos:
            problemas.append(f"ejemplo {i}: text_input duplicado")

        vistos.add(ej.text_input)

        try:
            salida = json.loads(ej.output)

        except json.JSONDecodeError:
            problemas.append(f"ejemplo {i}: output no es JSON valido")
            continue

        for clave in claves_esperadas:
            if clave not in salida:
                problemas.append(
                    f'ejemplo {i}: output no tiene la clave "{clave}"'
                )

    return problemas

# Convertir los ejemplos al formato del SDK

examples = [
    types.TuningExample(
        text_input=texto,
        output=json.dumps(salida, ensure_ascii=False)
    )
    for texto, salida in ejemplos_raw
]

print(len(examples), "ejemplos construidos")
print(examples[0])

print("\nBalance por intención:")
print(chequear_balance(ejemplos_raw, "intencion"))

print("\nBalance por prioridad:")
print(chequear_balance(ejemplos_raw, "prioridad"))

print("\nValidación del dataset:")

problemas = validar_dataset(
    examples,
    claves_esperadas=("intencion", "prioridad")
)

print(f"{len(examples)} ejemplos, {len(problemas)} problemas encontrados")

for p in problemas:
    print(" -", p)