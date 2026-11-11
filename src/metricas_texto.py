from collections import Counter
from src.pipeline_texto import procesar_texto

def contar_coincidencias(tokens_referencia, tokens_respuesta):

    conteo_referencia = Counter(tokens_referencia)
    conteo_respuesta = Counter(tokens_respuesta)

    interseccion = conteo_referencia & conteo_respuesta

    return sum(interseccion.values())

def calcular_precision_cobertura_f1(
    tokens_referencia,
    tokens_respuesta
):
    coincidencias = contar_coincidencias(
        tokens_referencia,
        tokens_respuesta
    )

    if not tokens_respuesta or not tokens_referencia:
        return {
            "precision": 0.0,
            "cobertura": 0.0,
            "f1": 0.0
        }

    precision = coincidencias / len(tokens_respuesta)

    cobertura = coincidencias / len(tokens_referencia)

    if precision + cobertura == 0:
        f1 = 0.0
    else:
        f1 = (
            2 * precision * cobertura
            / (precision + cobertura)
        )

    resultado = {
        "precision": precision,
        "cobertura": cobertura,
        "f1": f1
    }

    return resultado

def calcular_metricas(texto_referencia, texto_respuesta):

    tokens_referencia = procesar_texto(texto_referencia)

    tokens_respuesta = procesar_texto(texto_respuesta)

    return calcular_precision_cobertura_f1(
        tokens_referencia,
        tokens_respuesta
    )

if __name__ == "__main__":

    referencia = ["el", "gato", "duerme", "en", "el", "sofa"]

    respuesta = [
        "el", "gato", "duerme", "en", "el",
        "sillon", "todo", "el", "dia"
    ]

    resultado = calcular_precision_cobertura_f1(
        referencia,
        respuesta
    )

    print(resultado)

    referencia_texto = (
        "Para calcular el costo de una torta considera "
        "ingredientes, mano de obra y costos indirectos."
    )

    respuesta_texto = (
        "Debes considerar ingredientes, mano de obra, "
        "gas y electricidad."
    )

    resultado = calcular_metricas(
        referencia_texto,
        respuesta_texto
    )

    print("\nMétricas integradas:")
    print(resultado)

    referencia = procesar_texto("Python no es un lenguaje compilado.")
    respuesta = procesar_texto("Python es un lenguaje compilado.")

    resultado = calcular_precision_cobertura_f1(referencia, respuesta)

    print("\nEJEMPLO DE NEGACION:")
    print(resultado)

    referencia = procesar_texto("Python fue creado en 1991.")
    respuesta = procesar_texto("Python fue creado en 1989.")

    resultado = calcular_precision_cobertura_f1(referencia, respuesta)

    print("\nEJEMPLO DE DATO EQUIVOCADO:")
    print(resultado)