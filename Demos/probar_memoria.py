
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from src.agente_financiero import construir_agente_con_memoria

load_dotenv()

modelo = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

agente = construir_agente_con_memoria(modelo)

config = {
    "configurable": {
        "session_id": "empresa_001"
    }
}

# Primer turno
resultado_1 = agente.invoke(
    {
        "entrada": (
            "Mi empresa tiene ingresos de 10 millones, "
            "costos de 5 millones y gastos de 2 millones. "
            "Analiza su situación financiera."
        )
    },
    config
)

print("\nPRIMERA RESPUESTA:")
print(resultado_1["output"])

# Segundo turno: no repetimos las cifras
resultado_2 = agente.invoke(
    {
        "entrada": (
            "¿Qué pasa si mis gastos aumentan "
            "a 3 millones?"
        )
    },
    config
)

print("\nSEGUNDA RESPUESTA:")
print(resultado_2["output"])

# Segunda empresa: sesión independiente
config_empresa_2 = {
    "configurable": {
        "session_id": "empresa_002"
    }
}

resultado_3 = agente.invoke(
    {
        "entrada": (
            "¿Cuáles son los ingresos y costos "
            "que te informé anteriormente?"
        )
    },
    config_empresa_2
)

print("\nRESPUESTA EMPRESA 2:")
print(resultado_3["output"])

# Verificar cantidad de mensajes por sesión
from src.agente_financiero import obtener_historial

print(
    "\nMensajes empresa 001:",
    len(obtener_historial("empresa_001").messages)
)

print(
    "Mensajes empresa 002:",
    len(obtener_historial("empresa_002").messages)
)