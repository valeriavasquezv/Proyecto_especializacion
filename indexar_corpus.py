
import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# Cargar variables de entorno
load_dotenv()

# 1. Corpus: documentos de conocimiento de PymeCopilot
corpus = [
    "La herramienta calcular_indicadores_financieros recibe ingresos, costos y gastos. Requiere ingresos mayores que cero y calcula utilidad y margen de utilidad.",
    "La herramienta de conceptos financieros permite consultar liquidez, EBITDA, capital de trabajo, punto de equilibrio y margen de utilidad.",
    "El agente financiero utiliza herramientas para responder consultas y limita su ejecución a un máximo de cinco iteraciones.",
    "El cliente Gemini calcula el costo de una llamada usando promptTokenCount y candidatesTokenCount, junto con las tarifas de entrada y salida.",
    "El cliente reintenta errores TimeoutError hasta tres intentos, con espera exponencial y un máximo configurable. Los errores ValueError no se reintentan."
]

# 2. Dividir los documentos en fragmentos
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=30
)

chunks = splitter.create_documents(corpus)

# 3. Crear el modelo de embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# 4. Guardar documentos y embeddings en Chroma
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="vectorstore/"
)

print(f"Indexación completada: {len(chunks)} fragmentos almacenados.")
