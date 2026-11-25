
import json
from pathlib import Path

ARCHIVO_REGISTRO = Path(
    "evaluacion/registros_latencia_costo.jsonl"
)


def cargar_registros():
    """
    Lee el archivo JSONL y devuelve una lista
    de registros en formato diccionario.
    """

    if not ARCHIVO_REGISTRO.exists():
        print("No existe todavía el archivo de registros.")
        return []

    registros = []

    with ARCHIVO_REGISTRO.open(
        "r",
        encoding="utf-8"
    ) as archivo:

        for linea in archivo:
            if linea.strip():
                registros.append(json.loads(linea))

    return registros

def calcular_resumen(registros):
    """
    Calcula indicadores promedio de las ejecuciones RAG.
    """

    if not registros:
        print("No hay registros para analizar.")
        return None

    cantidad = len(registros)

    promedio_recuperacion = sum(
        r["latencia_recuperacion_seg"] for r in registros
    ) / cantidad

    promedio_generacion = sum(
        r["latencia_generacion_seg"] for r in registros
    ) / cantidad

    promedio_total = sum(
        r["latencia_total_seg"] for r in registros
    ) / cantidad

    promedio_tokens = sum(
        r["total_tokens"] for r in registros
    ) / cantidad

    costo_total = sum(
        r["costo_usd"] for r in registros
    )

    print("\n=== RESUMEN DE RENDIMIENTO RAG ===")
    print(f"Ejecuciones analizadas: {cantidad}")
    print(f"Latencia promedio recuperación: {promedio_recuperacion:.3f} s")
    print(f"Latencia promedio generación: {promedio_generacion:.3f} s")
    print(f"Latencia promedio total: {promedio_total:.3f} s")
    print(f"Promedio de tokens por consulta: {promedio_tokens:.1f}")
    print(f"Costo acumulado: US$ {costo_total:.8f}")

    return {
        "ejecuciones": cantidad,
        "latencia_promedio_recuperacion": promedio_recuperacion,
        "latencia_promedio_generacion": promedio_generacion,
        "latencia_promedio_total": promedio_total,
        "promedio_tokens": promedio_tokens,
        "costo_total_usd": costo_total
    }

def calcular_resumen_por_k(registros):
    if not registros:
        return

    grupos = {}

    for registro in registros:
        k = registro["k"]
        grupos.setdefault(k, []).append(registro)

    print("\n=== COMPARACIÓN DE CONFIGURACIONES K ===")

    for k in sorted(grupos):
        ejecuciones = grupos[k]
        cantidad = len(ejecuciones)

        promedio_recuperacion = sum(
            r["latencia_recuperacion_seg"] for r in ejecuciones
        ) / cantidad

        promedio_generacion = sum(
            r["latencia_generacion_seg"] for r in ejecuciones
        ) / cantidad

        promedio_total = sum(
            r["latencia_total_seg"] for r in ejecuciones
        ) / cantidad

        promedio_tokens = sum(
            r["total_tokens"] for r in ejecuciones
        ) / cantidad

        costo_total = sum(
            r["costo_usd"] for r in ejecuciones
        )

        print(f"\n--- K={k} ---")
        print(f"Ejecuciones: {cantidad}")
        print(f"Recuperación promedio: {promedio_recuperacion:.3f} s")
        print(f"Generación promedio: {promedio_generacion:.3f} s")
        print(f"Latencia total promedio: {promedio_total:.3f} s")
        print(f"Tokens promedio: {promedio_tokens:.1f}")
        print(f"Costo acumulado: US$ {costo_total:.8f}")


def validar_registros(registros):
    """
    Comprueba que los registros tengan los campos
    necesarios y valores numéricos válidos.
    """

    campos_obligatorios = [
        "fecha",
        "pregunta",
        "k",
        "latencia_recuperacion_seg",
        "latencia_generacion_seg",
        "latencia_total_seg",
        "tokens_entrada",
        "tokens_salida",
        "total_tokens",
        "costo_usd"
    ]

    errores = []

    for i, registro in enumerate(registros, start=1):

        faltantes = [
            campo for campo in campos_obligatorios
            if campo not in registro
        ]

        if faltantes:
            errores.append(
                f"Registro {i}: faltan campos {faltantes}"
            )
            continue

        if registro["total_tokens"] != (
            registro["tokens_entrada"]
            + registro["tokens_salida"]
        ):
            errores.append(
                f"Registro {i}: total de tokens inconsistente"
            )

        campos_numericos = [
            "latencia_recuperacion_seg",
            "latencia_generacion_seg",
            "latencia_total_seg",
            "tokens_entrada",
            "tokens_salida",
            "total_tokens",
            "costo_usd"
        ]

        for campo in campos_numericos:
            valor = registro[campo]

            if not isinstance(valor, (int, float)) or valor < 0:
                errores.append(
                    f"Registro {i}: valor inválido en {campo}"
                )

    if errores:
        print("\n=== ERRORES DE VALIDACIÓN ===")
        for error in errores:
            print(error)
        return False

    print("\n[OK] Todos los registros son válidos.")
    return True

if __name__ == "__main__":
    registros = cargar_registros()

    if registros and validar_registros(registros):
        calcular_resumen(registros)
        calcular_resumen_por_k(registros)