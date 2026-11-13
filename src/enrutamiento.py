from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableBranch,
    RunnablePassthrough
)

def construir_paso_clasificacion(modelo):

    plantilla_clasificacion = PromptTemplate.from_template(
        """
        Clasifica la siguiente solicitud financiera en una sola
        palabra: consulta, problema o mejora.

        - consulta: busca información o explicación financiera.
        - problema: informa una dificultad o riesgo financiero.
        - mejora: solicita ideas para mejorar resultados.

        Responde solamente con la categoría.

        Solicitud: {mensaje}
        """
    )

    return (
        plantilla_clasificacion
        | modelo
        | StrOutputParser()
        | (lambda texto: texto.strip().lower())
    )

def construir_cadena_con_enrutamiento(
    paso_clasificacion,
    cadena_consulta=None,
    cadena_problema=None,
    cadena_mejora=None
):

    # Rutas especializadas
    cadena_consulta = cadena_consulta or RunnablePassthrough()
    cadena_problema = cadena_problema or RunnablePassthrough()
    cadena_mejora = cadena_mejora or RunnablePassthrough()

    # Condiciones de bifurcación
    bifurcacion = RunnableBranch(
        (
            lambda x: x["categoria"] == "problema",
            cadena_problema
        ),
        (
            lambda x: x["categoria"] == "mejora",
            cadena_mejora
        ),
        cadena_consulta
    )

    # Conserva el mensaje original y agrega su categoría
    return (
        RunnablePassthrough.assign(
            categoria=paso_clasificacion
        )
        | bifurcacion
    )

def construir_rutas(modelo):

    # Ruta 1: consultas financieras
    cadena_consulta = (
        PromptTemplate.from_template(
            """
            Responde la siguiente consulta financiera
            de manera clara y precisa.

            Si faltan datos para responder, indícalo.

            Consulta: {mensaje}
            """
        )
        | modelo
        | StrOutputParser()
    )

    # Ruta 2: problemas financieros
    cadena_problema = (
        PromptTemplate.from_template(
            """
            Analiza el siguiente problema financiero.

            Identifica posibles causas, riesgos y consecuencias.
            No inventes datos que no hayan sido proporcionados.

            Problema: {mensaje}
            """
        )
        | modelo
        | StrOutputParser()
    )

    # Ruta 3: oportunidades de mejora
    cadena_mejora = (
        PromptTemplate.from_template(
            """
            Analiza la siguiente oportunidad de mejora financiera.

            Propón recomendaciones concretas y explica
            qué beneficios podrían generar.

            No inventes información financiera.

            Solicitud: {mensaje}
            """
        )
        | modelo
        | StrOutputParser()
    )

    return {
        "consulta": cadena_consulta,
        "problema": cadena_problema,
        "mejora": cadena_mejora
    }

def construir_flujo_completo(modelo):

    paso_clasificacion = construir_paso_clasificacion(modelo)

    rutas = construir_rutas(modelo)

    return construir_cadena_con_enrutamiento(
        paso_clasificacion=paso_clasificacion,
        cadena_consulta=rutas["consulta"],
        cadena_problema=rutas["problema"],
        cadena_mejora=rutas["mejora"]
    )
