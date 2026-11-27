
import os
from types import SimpleNamespace

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.types import Command

from src.agente_supervisado import construir_agente_supervisado
from src.trazabilidad import registrar_traza


def extraer_texto(mensaje):
    contenido = mensaje.content

    if isinstance(contenido, str):
        return contenido

    if isinstance(contenido, list):
        return "\n".join(
            bloque.get("text", "")
            for bloque in contenido
            if isinstance(bloque, dict)
            and bloque.get("type") == "text"
        )

    return str(contenido)


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

    ejecutor = construir_agente_supervisado(modelo)

    consultas = [
        "¿Por qué es importante que una empresa tenga una buena gestión financiera?",
        "Calcula mis indicadores financieros: ingresos 10000000, costos 5000000 y gastos 2000000."
    ]

    session_id = "empresa_001"

    config = {
        "configurable": {
            "thread_id": session_id
        }
    }

    for consulta in consultas:
        print("\n" + "=" * 70)
        print("CONSULTA:", consulta)

        operacion_rechazada = False

        resultado = ejecutor.invoke(
            {
                "messages": [
                    {"role": "user", "content": consulta}
                ]
            },
            config=config
        )

        while resultado.get("__interrupt__"):
            print("\nSUPERVISIÓN HUMANA ACTIVADA")
            print(resultado["__interrupt__"])

            decision = input(
                "\n¿Apruebas ejecutar la operación? (s/n): "
            ).strip().lower()

            aprobada = decision == "s"

            
            if not aprobada:
                operacion_rechazada = True
                break

            respuesta = {
                "decisions": [
                    {
                        "type": "approve"
                    }
                ]
            }

            resultado = ejecutor.invoke(
                Command(resume=respuesta),
                config=config
            )

        mensajes = resultado.get("messages", [])

        # Registrar únicamente herramientas que realmente
        # generaron un mensaje de ejecución (ToolMessage).
        herramientas = [
            mensaje.name
            for mensaje in mensajes
            if isinstance(mensaje, ToolMessage)
            and mensaje.name
        ]

        pasos_traza = [
            (SimpleNamespace(tool=nombre), None)
            for nombre in herramientas
        ]

        trace_id = registrar_traza(
            session_id=session_id,
            entrada=consulta,
            resultado={
                "intermediate_steps": pasos_traza
            }
        )

        print("\nTRACE ID:", trace_id)

        print("\nRESPUESTA:")

        if operacion_rechazada:
            print(
                "La operación fue rechazada por el revisor humano. "
                "No se ejecutó el cálculo financiero y no se "
                "generaron resultados."
            )
        else:
            respuesta_mostrada = False

            for mensaje in reversed(mensajes):
                if isinstance(mensaje, AIMessage) and mensaje.content:
                    print(extraer_texto(mensaje))
                    respuesta_mostrada = True
                    break

            if not respuesta_mostrada:
                print("El agente no generó una respuesta.")

        print("\nHERRAMIENTAS REALMENTE EJECUTADAS:")

        if herramientas:
            for herramienta in herramientas:
                print("-", herramienta)
        else:
            print("Ninguna")


if __name__ == "__main__":
    main()
