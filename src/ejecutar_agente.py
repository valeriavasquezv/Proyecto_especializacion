
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from src.agente_financiero import construir_agente_con_memoria
from src.trazabilidad import registrar_traza


def main():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "No se encontró GEMINI_API_KEY. "
            "Revisa tu archivo .env."
        )

    modelo = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        google_api_key=api_key,
        temperature=0
    )

    ejecutor = construir_agente_con_memoria(modelo)

    consultas = [
        "¿Por qué es importante que una empresa tenga una buena gestión financiera?",
        "Calcula mis indicadores financieros: ingresos 10000000, costos 5000000 y gastos 2000000."
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

        registrar_traza(
            session_id="empresa_001",
            entrada=consulta,
            resultado=resultado
        )

        print("\nRESPUESTA:", resultado["output"])

        print("\nHERRAMIENTAS UTILIZADAS:")

        for accion, observacion in resultado.get(
            "intermediate_steps", []
        ):
            print("Herramienta:", accion.tool)
            print("Argumentos:", accion.tool_input)
            print("Resultado:", observacion)


if __name__ == "__main__":
    main()
