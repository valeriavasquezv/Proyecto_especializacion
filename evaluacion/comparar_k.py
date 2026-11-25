
from evaluacion.registro_rag import ejecutar_rag_medido

PREGUNTA = "¿Qué calcula la herramienta de indicadores financieros?"

def comparar_configuraciones():
    resultados = []

    for k in [1, 2, 3]:
        print(f"\n{'=' * 50}")
        print(f"EJECUTANDO PRUEBA CON K={k}")
        print(f"{'=' * 50}")

        respuesta, citas, registro = ejecutar_rag_medido(
            pregunta=PREGUNTA,
            k=k
        )

        resultados.append(registro)

        print("\nRespuesta:", respuesta)
        print("Fuentes:", citas)
        print(f"Latencia recuperación: {registro['latencia_recuperacion_seg']:.3f} s")
        print(f"Latencia generación: {registro['latencia_generacion_seg']:.3f} s")
        print(f"Latencia total: {registro['latencia_total_seg']:.3f} s")
        print(f"Tokens entrada: {registro['tokens_entrada']}")
        print(f"Tokens salida: {registro['tokens_salida']}")
        print(f"Costo estimado: US$ {registro['costo_usd']:.8f}")

    return resultados


if __name__ == "__main__":
    comparar_configuraciones()
