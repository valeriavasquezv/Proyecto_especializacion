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

ejecutor = construir_agente_con_memoria(modelo)

consultas = [
    "¿Por qué es importante que una empresa tenga "
    "una buena gestión financiera?"
]

config = {
    "configurable": {
        "session_id": "empresa_001"
    }
}

for consulta in consultas:

    print("\n" + "=" * 70)
    print("CONSULTA:", consulta)

    resultado = ejecutor.invoke(
        {"entrada": consulta},
        config=config
    )

    print("\nRESPUESTA:", resultado["output"])

    print("\nHERRAMIENTAS UTILIZADAS:")

    for accion, observacion in resultado["intermediate_steps"]:
        print("Herramienta:", accion.tool)
        print("Argumentos:", accion.tool_input)
        print("Resultado:", observacion)

