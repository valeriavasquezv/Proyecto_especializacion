
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from src.cadena_tres_pasos import construir_cadena

# Cargar variables de entorno
load_dotenv()

# Conectar con Gemini
modelo = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

# Construir la cadena
cadena = construir_cadena(modelo)

# Datos de una empresa de transporte
datos = {
    "tipo_negocio": "empresa de transporte",
    "ingresos": 8000000,
    "costos": 5000000,
    "gastos": 1500000
}

# Ejecutar los tres pasos
resultado = cadena.invoke(datos)

print("\n===== RESULTADO DE PYME COPILOT =====")
print(resultado)
