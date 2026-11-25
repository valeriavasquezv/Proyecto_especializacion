
import os
from dotenv import load_dotenv
import chromadb

load_dotenv()

RUTA_VECTORSTORE = "vectorstore"
COLECCION = "langchain"

IDS_ESPERADOS = [
    "chunk_0",
    "chunk_1",
    "chunk_2",
    "chunk_3",
    "chunk_4"
]


def ejecutar_preflight():
    print("\n=== PREFLIGHT PYME COPILOT ===")

    # 1. Comprobar API key
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        print("[OK] GEMINI_API_KEY configurada")
    else:
        print("[ERROR] GEMINI_API_KEY no encontrada")

    # 2. Comprobar vectorstore
    if not os.path.isdir(RUTA_VECTORSTORE):
        print("[ERROR] No existe la carpeta vectorstore")
        return

    print("[OK] Carpeta vectorstore encontrada")

    # 3. Conectar con Chroma
    try:
        cliente = chromadb.PersistentClient(
            path=RUTA_VECTORSTORE
        )

        coleccion = cliente.get_collection(
            name=COLECCION
        )

        print("[OK] Colección Chroma encontrada")

        # 4. Comprobar cantidad de documentos
        cantidad = coleccion.count()
        print(f"Documentos almacenados: {cantidad}")

        # 5. Comprobar identificadores
        resultado = coleccion.get(
            ids=IDS_ESPERADOS
        )

        ids_encontrados = resultado["ids"]

        if set(ids_encontrados) == set(IDS_ESPERADOS):
            print("[OK] Los cinco fragmentos esperados están presentes")
        else:
            print("[ERROR] Faltan fragmentos")
            print("Encontrados:", ids_encontrados)

    except Exception as error:
        print("[ERROR] No se pudo verificar Chroma")
        print(type(error).__name__, error)


if __name__ == "__main__":
    ejecutar_preflight()
