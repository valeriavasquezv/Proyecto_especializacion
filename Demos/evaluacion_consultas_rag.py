
import sys
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Permitir importar desde la raíz del proyecto
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# 1. Configuración de consultas de evaluación
CONSULTAS = [
    {
        "pregunta": "¿Cómo se calcula el margen de utilidad?",
        "tipo": "pertinente",
        "fuentes_esperadas": ["indicadores_financieros"]
    },
    {
        "pregunta": "¿Qué indicadores financieros calcula la herramienta?",
        "tipo": "pertinente",
        "fuentes_esperadas": ["indicadores_financieros", "conceptos_financieros"]
    },
    {
        "pregunta": "¿Qué es el EBITDA?",
        "tipo": "pertinente",
        "fuentes_esperadas": ["conceptos_financieros"]
    },
    {
        "pregunta": "¿Cuántas veces puede ejecutarse el agente?",
        "tipo": "pertinente",
        "fuentes_esperadas": ["agente_financiero"]
    },
    {
        "pregunta": "¿Cómo se calcula el costo de una llamada a Gemini?",
        "tipo": "pertinente",
        "fuentes_esperadas": ["cliente_gemini"]
    },
    {
        "pregunta": "¿Cuál es la dirección comercial de la empresa?",
        "tipo": "irrelevante",
        "fuentes_esperadas": []
    },
    {
        "pregunta": "¿Quiénes son los trabajadores de la empresa?",
        "tipo": "irrelevante",
        "fuentes_esperadas": []
    },
    {
        "pregunta": "¿Cuál es el horario de atención del negocio?",
        "tipo": "irrelevante",
        "fuentes_esperadas": []
    },
    {
        "pregunta": "¿Qué proveedores tiene la empresa?",
        "tipo": "irrelevante",
        "fuentes_esperadas": []
    },
    {
        "pregunta": "¿Dónde se encuentra ubicada la oficina?",
        "tipo": "irrelevante",
        "fuentes_esperadas": []
    }
]

# 2. Inicializar embeddings y Chroma
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

vectorstore = Chroma(
    persist_directory="vectorstore/",
    embedding_function=embeddings
)

# 3. Recuperar documentos y comparar resultados
def evaluar_recuperacion(k=3):

    VP = 0
    VN = 0
    FP = 0
    FN = 0
    suma_recall = 0
    suma_precision = 0
    consultas_con_fuentes = 0

    UMBRAL_EXPERIMENTAL = 0.52

    for numero, consulta in enumerate(CONSULTAS, start=1):

        pregunta = consulta["pregunta"]

        resultados = vectorstore.similarity_search_with_relevance_scores(
            pregunta,
            k=k
        )

        if not resultados:
            puntaje_maximo = 0
        else:
            puntaje_maximo = max(
                puntaje for doc, puntaje in resultados
            )

        aceptada = puntaje_maximo >= UMBRAL_EXPERIMENTAL
        pertinente = consulta["tipo"] == "pertinente"

        if pertinente and aceptada:
            VP += 1
        elif pertinente and not aceptada:
            FN += 1
        elif not pertinente and aceptada:
            FP += 1
        else:
            VN += 1

        fuentes_recuperadas = [
            doc.metadata.get("fuente", "desconocida")
            for doc, puntaje in resultados
        ]

        aciertos = set(fuentes_recuperadas) & set(
            consulta["fuentes_esperadas"]
        )

                # Evaluación de recuperación documental
        fuentes_esperadas = consulta["fuentes_esperadas"]

        if fuentes_esperadas:
            recall_k = len(aciertos) / len(fuentes_esperadas)
            precision_k = (
            len(aciertos) / len(resultados)
            if resultados else 0
        )

            suma_recall += recall_k
            suma_precision += precision_k
            consultas_con_fuentes += 1

            print(f"Recall@{k}: {recall_k:.2%}")
            print(f"Precision@{k}: {precision_k:.2%}")

        print("\n" + "=" * 60)
        print(f"CONSULTA {numero}")
        print("Pregunta:", pregunta)
        print("Tipo:", consulta["tipo"])
        print("Puntaje máximo:", round(puntaje_maximo, 4))
        print("Umbral experimental:", UMBRAL_EXPERIMENTAL)
        print("Decisión:", "ACEPTAR" if aceptada else "RECHAZAR")
        print("Fuentes esperadas:", consulta["fuentes_esperadas"])
        print("Fuentes recuperadas correctamente:", sorted(aciertos))

        print("\nDocumentos recuperados:")

        for doc, puntaje in resultados:
            print(
                f"- {doc.metadata.get('fuente')}: "
                f"{puntaje:.4f}"
            )

    # Cálculo de métricas

    total = VP + VN + FP + FN

    precision = VP / (VP + FP) if VP + FP else 0
    sensibilidad = VP / (VP + FN) if VP + FN else 0
    especificidad = VN / (VN + FP) if VN + FP else 0
    exactitud = (VP + VN) / total if total else 0

    print("\n" + "=" * 60)
    print("RESUMEN DE EVALUACIÓN RAG")
    print("=" * 60)

    print("Verdaderos positivos:", VP)
    print("Verdaderos negativos:", VN)
    print("Falsos positivos:", FP)
    print("Falsos negativos:", FN)

    print(f"\nPrecisión: {precision:.2%}")
    print(f"Sensibilidad: {sensibilidad:.2%}")
    print(f"Especificidad: {especificidad:.2%}")
    print(f"Exactitud: {exactitud:.2%}")

        # Promedio de métricas de recuperación

    if consultas_con_fuentes > 0:
        recall_promedio = suma_recall / consultas_con_fuentes
        precision_promedio = suma_precision / consultas_con_fuentes

        print("\n" + "=" * 60)
        print("RESUMEN DE RECUPERACIÓN DOCUMENTAL")
        print("=" * 60)

        print(f"Recall@{k} promedio: {recall_promedio:.2%}")
        print(f"Precision@{k} promedio: {precision_promedio:.2%}")
def comparar_k():

    valores_k = [1, 2, 3]

    print("\n" + "=" * 60)
    print("EXPERIMENTO COMPARATIVO DE K")
    print("=" * 60)

    for k in valores_k:

        suma_recall = 0
        suma_precision = 0
        total_consultas = 0

        print(f"\nEVALUACIÓN CON K = {k}")

        for consulta in CONSULTAS:

            if consulta["tipo"] != "pertinente":
                continue

            pregunta = consulta["pregunta"]

            resultados = vectorstore.similarity_search_with_relevance_scores(
                pregunta,
                k=k
            )

            fuentes_recuperadas = {
                doc.metadata.get("fuente", "desconocida")
                for doc, puntaje in resultados
            }

            fuentes_esperadas = set(
                consulta["fuentes_esperadas"]
            )

            aciertos = fuentes_recuperadas & fuentes_esperadas

            recall_k = (
                len(aciertos) / len(fuentes_esperadas)
                if fuentes_esperadas else 0
            )

            precision_k = (
                len(aciertos) / len(resultados)
                if resultados else 0
            )

            suma_recall += recall_k
            suma_precision += precision_k
            total_consultas += 1

        recall_promedio = suma_recall / total_consultas
        precision_promedio = suma_precision / total_consultas

        print(f"Recall@{k} promedio: {recall_promedio:.2%}")
        print(f"Precision@{k} promedio: {precision_promedio:.2%}")

if __name__ == "__main__":
    comparar_k()
    evaluar_recuperacion()