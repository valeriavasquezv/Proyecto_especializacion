
import os
import hashlib
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

# 1. Corpus propio
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

# 2. División en fragmentos
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=30
)

chunks = splitter.create_documents(corpus, metadatas=metadatos)

# 3. Identificadores estables por fuente y contenido
ids = []

for chunk in chunks:
    contenido = chunk.page_content
    fuente = chunk.metadata["fuente"]

    identificador = hashlib.sha256(
        f"{fuente}:{contenido}".encode("utf-8")
    ).hexdigest()

    ids.append(identificador)

    # Identifica los documentos administrados por este indexador
    chunk.metadata["gestion_indexador"] = "indexar_corpus"

# 4. Configuración de embeddings
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("No se encontró GEMINI_API_KEY en el archivo .env")

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=api_key
)

# 5. Abrir el vector store existente o crear uno nuevo
vectorstore = Chroma(
    persist_directory="vectorstore/",
    embedding_function=embeddings
)

# 6. Consultar los documentos que ya están almacenados
existentes = vectorstore.get(include=["metadatas"])

ids_existentes = existentes["ids"]
metadatos_existentes = existentes["metadatas"]

# Identificar los documentos administrados por este indexador
ids_administrados = {
    identificador
    for identificador, metadata in zip(
        ids_existentes, metadatos_existentes
    )
    if metadata
    and metadata.get("gestion_indexador") == "indexar_corpus"
}

# 7. Identificar documentos nuevos
ids_nuevos = [
    identificador
    for identificador in ids
    if identificador not in ids_existentes
]

documentos_nuevos = [
    chunk
    for chunk, identificador in zip(chunks, ids)
    if identificador in ids_nuevos
]

# 8. Agregar solamente los documentos nuevos
if documentos_nuevos:
    vectorstore.add_documents(
        documents=documentos_nuevos,
        ids=ids_nuevos
    )

# 9. Eliminar documentos administrados que ya no pertenecen al corpus
ids_actuales = set(ids)

ids_obsoletos = list(
    ids_administrados - ids_actuales
)

if ids_obsoletos:
    vectorstore.delete(ids=ids_obsoletos)

# 10. Migrar los identificadores antiguos del indexador original
# Se hace después de agregar los documentos con identificadores estables.
ids_legacy = [
    identificador
    for identificador in ids_existentes
    if identificador.startswith("chunk_")
    and identificador[6:].isdigit()
]

if ids_legacy:
    vectorstore.delete(ids=ids_legacy)

# 11. Resumen
total = vectorstore._collection.count()

print("\n=== INDEXACIÓN INCREMENTAL ===")
print(f"Fragmentos del corpus: {len(chunks)}")
print(f"Documentos nuevos agregados: {len(documentos_nuevos)}")
print(f"Documentos obsoletos eliminados: {len(ids_obsoletos)}")
print(f"Identificadores antiguos migrados: {len(ids_legacy)}")
print(f"Total de documentos en Chroma: {total}")
print("\nIndexación incremental completada.")
