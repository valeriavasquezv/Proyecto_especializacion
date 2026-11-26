
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()


PROMPT_TEMPLATE = """
Responde la pregunta usando SOLO el contexto de abajo.

Cita la fuente de cada afirmación con su número entre corchetes,
por ejemplo [1].

Si el contexto no alcanza para responder,
dilo explícitamente en vez de inventar.

CONTEXTO:
{contexto}

PREGUNTA:
{pregunta}

RESPUESTA:
"""


def formatear_contexto(chunks_recuperados):
    lineas = []
    citas = {}

    for i, doc in enumerate(chunks_recuperados, start=1):
        fuente = doc.metadata.get("fuente", "desconocida")
        lineas.append(f"[{i}] {doc.page_content}")
        citas[i] = fuente

    contexto = "\n\n".join(lineas)

    return contexto, citas


def recuperar_documentos(pregunta, k=3):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    vectorstore = Chroma(
        persist_directory="vectorstore/",
        embedding_function=embeddings
    )

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": k}
    )

    return retriever.invoke(pregunta)

def recuperar_documentos_con_puntajes(pregunta, k=2):

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    vectorstore = Chroma(
        persist_directory="vectorstore/",
        embedding_function=embeddings
    )

    resultados = vectorstore.similarity_search_with_relevance_scores(
        pregunta,
        k=k
    )

    return resultados

def construir_prompt(pregunta, k=3):
    chunks = recuperar_documentos(pregunta, k)

    contexto, citas = formatear_contexto(chunks)

    prompt = PROMPT_TEMPLATE.format(
        contexto=contexto,
        pregunta=pregunta
    )

    return prompt, citas


import re
from src.cliente import consultar_modelo



def generar_respuesta(pregunta, k=2):

    UMBRAL_RELEVANCIA = 0.52

    resultados = recuperar_documentos_con_puntajes(
        pregunta,
        k=k
    )

    if not resultados:
        return (
            "No encontré información suficiente para responder.",
            {}
        )

    puntaje_maximo = max(
        puntaje for doc, puntaje in resultados
    )

    if puntaje_maximo < UMBRAL_RELEVANCIA:
        return (
            "No encontré información suficientemente relevante "
            "en la base de conocimiento para responder esta consulta.",
            {}
        )

    chunks = [
        doc for doc, puntaje in resultados
    ]

    contexto, citas = formatear_contexto(chunks)

    prompt = PROMPT_TEMPLATE.format(
        contexto=contexto,
        pregunta=pregunta
    )

    system_instruction = (
        "Eres un asistente financiero. "
        "Responde utilizando exclusivamente el contexto "
        "proporcionado y cita las fuentes con [1], [2], etc. "
        "Si la información no es suficiente, indícalo."
    )

    respuesta = consultar_modelo(
        pregunta=prompt,
        system_instruction=system_instruction
    )

    numeros_citados = re.findall(r"\[(\d+)\]", respuesta)

    fuentes_utilizadas = {}

    for numero in numeros_citados:
        indice = int(numero)

        if indice in citas:
            fuentes_utilizadas[indice] = citas[indice]
        else:
            fuentes_utilizadas[indice] = "CITA INVÁLIDA"

    return respuesta, fuentes_utilizadas