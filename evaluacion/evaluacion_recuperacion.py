from dotenv import load_dotenv

load_dotenv()
from datetime import datetime

def calcular_precision_at_k(ids_recuperados, ids_relevantes):
    """
    Calcula qué proporción de los documentos recuperados
    realmente son relevantes.
    """
    if not ids_recuperados:
        return 0.0

    relevantes_encontrados = sum(
        1 for documento in ids_recuperados
        if documento in ids_relevantes
    )

    return relevantes_encontrados / len(ids_recuperados)


def calcular_recall_at_k(ids_recuperados, ids_relevantes):
    """
    Calcula qué proporción de todos los documentos relevantes
    logró recuperar el sistema.
    """
    if not ids_relevantes:
        return 0.0

    relevantes_encontrados = sum(
        1 for documento in ids_recuperados
        if documento in ids_relevantes
    )

    return relevantes_encontrados / len(ids_relevantes)


def calcular_f1(precision, recall):
    """
    Combina precisión y exhaustividad en una sola métrica.
    """
    if precision + recall == 0:
        return 0.0

    return 2 * (precision * recall) / (precision + recall)



CASOS_EVALUACION = [
    {
        "pregunta": "¿Qué calcula la herramienta de indicadores financieros?",
        "ids_relevantes": {"indicadores_financieros"}
    },
    {
        "pregunta": "¿Qué condición deben cumplir los ingresos?",
        "ids_relevantes": {"indicadores_financieros"}
    },
    {
        "pregunta": "¿Qué conceptos financieros puede consultar el asistente?",
        "ids_relevantes": {"conceptos_financieros"}
    },
    {
        "pregunta": "¿Se puede consultar EBITDA?",
        "ids_relevantes": {"conceptos_financieros"}
    },
    {
        "pregunta": "¿Cuántas iteraciones puede ejecutar el agente?",
        "ids_relevantes": {"agente_financiero"}
    },
    {
        "pregunta": "¿Qué función cumple el agente financiero?",
        "ids_relevantes": {"agente_financiero"}
    },
    {
        "pregunta": "¿Qué datos utiliza Gemini para calcular el costo de una llamada?",
        "ids_relevantes": {"cliente_gemini"}
    },
    {
        "pregunta": "¿Qué contadores de tokens utiliza el cliente?",
        "ids_relevantes": {"cliente_gemini"}
    },
    {
        "pregunta": "¿Qué ocurre cuando se produce un TimeoutError?",
        "ids_relevantes": {"cliente_reintento"}
    },
    {
        "pregunta": "¿Qué errores no se vuelven a intentar?",
        "ids_relevantes": {"cliente_reintento"}
    }
]

def recuperar_ids(pregunta, k=3):
    from src.recuperacion_rag import recuperar_documentos

    documentos = recuperar_documentos(pregunta, k=k)

    return [
        doc.metadata.get("fuente", "desconocida")
        for doc in documentos
    ]

def evaluar_casos(k=3):
    resultados = []

    for caso in CASOS_EVALUACION:
        pregunta = caso["pregunta"]
        relevantes = caso["ids_relevantes"]

        recuperados = recuperar_ids(pregunta, k)

        p = calcular_precision_at_k(recuperados, relevantes)
        r = calcular_recall_at_k(recuperados, relevantes)
        f1 = calcular_f1(p, r)

        resultados.append({
            "pregunta": pregunta,
            "precision": p,
            "recall": r,
            "f1": f1
        })

        print(f"\nPregunta: {pregunta}")
        print(f"IDs recuperados: {recuperados}")
        print(f"IDs relevantes: {relevantes}")
        print(f"Precision@{k}: {p:.2%}")
        print(f"Recall@{k}: {r:.2%}")
        print(f"F1: {f1:.2%}")

    promedio_p = sum(x["precision"] for x in resultados) / len(resultados)
    promedio_r = sum(x["recall"] for x in resultados) / len(resultados)
    promedio_f1 = sum(x["f1"] for x in resultados) / len(resultados)

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    resumen = (
        f"\n{'=' * 55}\n"
        f"FECHA: {fecha}\n"
        f"K: {k}\n"
        f"CHUNK SIZE: 200\n"
        f"CHUNK OVERLAP: 30\n"
        f"TOTAL DE PREGUNTAS: {len(resultados)}\n"
        f"PROMEDIO PRECISION@{k}: {promedio_p:.2%}\n"
        f"PROMEDIO RECALL@{k}: {promedio_r:.2%}\n"
        f"PROMEDIO F1: {promedio_f1:.2%}\n"
        f"{'=' * 55}\n"
    )

    print("\nRESUMEN GENERAL")
    print(resumen)

    with open("resultados_evaluacion.txt", "a", encoding="utf-8") as archivo:
        archivo.write(resumen)

    print("Resultados guardados en resultados_evaluacion.txt")

    return resultados

if __name__ == "__main__":
    for k in [1, 2, 3]:
        print(f"\n\n{'#' * 55}")
        print(f"EVALUACIÓN CON K={k}")
        print(f"{'#' * 55}")

        evaluar_casos(k=k)