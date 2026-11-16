
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from src.enrutamiento import (
    construir_flujo_completo,
    procesar_mensaje_seguro
)

load_dotenv()

modelo = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

cadena = construir_flujo_completo(modelo)

solicitudes = [
    "¿Qué significa el margen de rentabilidad de una empresa?",
    "Mis gastos aumentaron y ahora tengo problemas para pagar mis obligaciones.",
    "Quiero mejorar la rentabilidad de mi empresa."
]

for mensaje in solicitudes:

    print("\n" + "=" * 60)
    print("SOLICITUD:", mensaje)

    resultado = procesar_mensaje_seguro(
        cadena,
        mensaje
    )

    print("\nRESPUESTA PYME COPILOT:")
    print(resultado)
