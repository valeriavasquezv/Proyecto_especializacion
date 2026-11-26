import sys
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Permitir importar módulos desde la raíz del proyecto
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

pregunta = "¿Qué herramientas utiliza el proyecto para recuperar información?"

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

vectorstore = Chroma(
    persist_directory="vectorstore/",
    embedding_function=embeddings
)

resultados = vectorstore.similarity_search_with_relevance_scores(
    pregunta,
    k=3
)

for i, (doc, puntaje) in enumerate(resultados, start=1):
    print(f"\n--- DOCUMENTO {i} ---")
    print("Fuente:", doc.metadata.get("fuente", "desconocida"))
    print("Puntaje de relevancia:", round(puntaje, 4))
    print("Contenido:", doc.page_content[:300])
