
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def construir_cadena(modelo):

    # PASO 1: Análisis financiero
    plantilla_analisis = PromptTemplate.from_template(
        """
        Analiza la situación financiera de esta empresa:

        Tipo de negocio: {tipo_negocio}
        Ingresos: {ingresos}
        Costos: {costos}
        Gastos: {gastos}

        Identifica los principales indicadores financieros
        y posibles problemas.
        """
    )

    # PASO 2: Diagnóstico
    plantilla_diagnostico = PromptTemplate.from_template(
        """
        A partir del siguiente análisis financiero:

        {analisis_financiero}

        Elabora un diagnóstico.
        Identifica las causas de los problemas financieros
        y explica sus posibles consecuencias.
        """
    )

    # PASO 3: Recomendaciones
    plantilla_recomendaciones = PromptTemplate.from_template(
        """
        Considerando el siguiente diagnóstico:

        {diagnostico}

        Propón tres recomendaciones concretas para mejorar
        la situación financiera de la empresa.

        Explica brevemente el beneficio esperado de cada acción.
        """
    )

    # Conexión de los tres pasos
    cadena = (
        plantilla_analisis
        | modelo
        | StrOutputParser()
        | (lambda analisis: {
            "analisis_financiero": analisis
        })
        | plantilla_diagnostico
        | modelo
        | StrOutputParser()
        | (lambda diagnostico: {
            "diagnostico": diagnostico
        })
        | plantilla_recomendaciones
        | modelo
        | StrOutputParser()
    )

    return cadena
