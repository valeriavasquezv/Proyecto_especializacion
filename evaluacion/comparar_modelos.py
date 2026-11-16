import time
from src.consumir_gemini import (
    armar_peticion,
    enviar_peticion,
    calcular_costo,
)

PRECIOS = {
    "gemini-3.1-flash-lite": {
        "entrada": 0.25 / 1_000_000,
        "salida": 1.50 / 1_000_000,
    },
        "gemini-3.5-flash-lite": {
        "entrada": 0.30 / 1_000_000,
        "salida": 2.50 / 1_000_000,
    },
}

modelos = [
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
]

pregunta = "Explica en dos frases qué es una variable en Python."

for modelo in modelos:
    latencias = []

    print(f"\nModelo: {modelo}")

    for intento in range(4):
        try:
            url, body = armar_peticion(pregunta, modelo=modelo)

            inicio = time.perf_counter()
            datos = enviar_peticion(url, body)
            fin = time.perf_counter()

            texto = datos["candidates"][0]["content"]["parts"][0]["text"]

            print("Respuesta del modelo:")
            print(texto)

            latencia = fin - inicio
            latencias.append(latencia)

            precios = PRECIOS[modelo]
            costo = calcular_costo(
                datos,
                precios["entrada"],
                precios["salida"],
            )

            print(f"Prueba {intento + 1}: {latencia:.2f} segundos")
            print(f"Costo estimado: US$ {costo:.8f}")

        except RuntimeError as error:
            print(f"Error en la prueba {intento + 1}: {error}")
            continue

    if latencias:
        promedio = sum(latencias) / len(latencias)
        print(f"Promedio: {promedio:.2f} segundos")
        print(f"Pruebas completadas: {len(latencias)} de 4")
    else:
        print("No se pudo calcular el promedio.")
