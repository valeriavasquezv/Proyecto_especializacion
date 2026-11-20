import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

corpus = [
    "La herramienta calcular_indicadores_financieros recibe ingresos, costos y gastos. Requiere ingresos mayores que cero y calcula utilidad y margen de utilidad.",
    "La herramienta de conceptos financieros permite consultar liquidez, EBITDA, capital de trabajo, punto de equilibrio y margen de utilidad.",
    "El agente financiero utiliza herramientas para responder consultas y limita su ejecución a un máximo de cinco iteraciones.",
    "El cliente Gemini calcula el costo de una llamada usando promptTokenCount y candidatesTokenCount, junto con las tarifas de entrada y salida.",
    "El cliente reintenta errores TimeoutError hasta tres intentos, con espera exponencial. Los errores ValueError no se reintentan."
]

metadatos = [
    {"fuente": "indicadores_financieros"},
    {"fuente": "conceptos_financieros"},
    {"fuente": "agente_financiero"},
    {"fuente": "cliente_gemini"},
    {"fuente": "cliente_reintento"}
]

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=30
)

chunks = splitter.create_documents(corpus, metadatas=metadatos)

ids = [f"chunk_{i}" for i in range(len(chunks))]

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    ids=ids,
    persist_directory="vectorstore/"
)

print(f"Indexación completada: {len(chunks)} fragmentos almacenados.")