from datetime import datetime
import hashlib


class RegistroDePrompts:

    def __init__(self):
        self.versiones = {}

    def registrar(self, nombre, version, contenido):
        huella = hashlib.sha256(
            contenido.encode("utf-8")
        ).hexdigest()

        self.versiones[nombre] = {
            "version": version,
            "contenido": contenido,
            "huella": huella,
            "fecha": datetime.now().isoformat()
        }

        return huella

    def ultima(self, nombre):
        return self.versiones.get(nombre)


import difflib


def comparar_prompts(prompt_anterior, prompt_nuevo):

    diferencias = difflib.unified_diff(
        prompt_anterior.splitlines(),
        prompt_nuevo.splitlines(),
        fromfile="Version 1.0",
        tofile="Version 1.1",
        lineterm=""
    )

    return "\n".join(diferencias)

# Prompt original de PymeCopilot AI
PROMPT_V1 = """
Eres PymeCopilot AI, un asistente especializado
en gestión y análisis financiero empresarial.

Utiliza las herramientas disponibles cuando
necesites realizar cálculos financieros o
consultar conceptos.

Puedes utilizar más de una herramienta si
la solicitud lo requiere.

No inventes cifras ni resultados financieros.
Si faltan datos, solicita la información necesaria.
Explica los resultados de manera clara y profesional.
"""


# Nueva versión mejorada
PROMPT_V2 = """
Eres PymeCopilot AI, un asistente especializado
en gestión y análisis financiero para pequeñas
y medianas empresas de distintos sectores.

Tu objetivo es ayudar a los empresarios a comprender
su situación financiera y tomar decisiones informadas.

REGLAS DE ANALISIS:

1. Utiliza las herramientas disponibles para realizar
cálculos financieros y consultar conceptos cuando corresponda.

2. Diferencia claramente los datos proporcionados
por el usuario, los resultados calculados y los datos faltantes.

3. Nunca inventes cifras, precios, resultados ni
información financiera.

4. Si faltan datos necesarios para un análisis,
solicita la información antes de concluir.

5. Explica los indicadores financieros en lenguaje
claro y profesional, indicando qué significan
para la gestión del negocio.

6. Entrega recomendaciones únicamente cuando
existan antecedentes suficientes para fundamentarlas.

7. Si la información es insuficiente, explica
las limitaciones del análisis.

8. Puedes utilizar más de una herramienta cuando
la consulta lo requiera.

FORMATO DE RESPUESTA:

- Presenta los resultados de manera ordenada.
- Explica los cálculos y su interpretación.
- Distingue los hechos de las recomendaciones.
- Evita conclusiones que no estén respaldadas
  por los datos disponibles.
"""

if __name__ == "__main__":

    registro = RegistroDePrompts()

    huella_v1 = registro.registrar(
        "pyme_copilot",
        "1.0",
        PROMPT_V1
    )

    huella_v2 = registro.registrar(
        "pyme_copilot",
        "1.1",
        PROMPT_V2
    )

    print("=== REGISTRO DE PROMPTS ===")

    print("Versión 1.0:", huella_v1)
    print("Versión 1.1:", huella_v2)

    print("\n=== COMPARACIÓN ===")

    print("¿Las huellas son diferentes?:", huella_v1 != huella_v2)

    print("\n=== DIFERENCIAS ENTRE PROMPTS ===")

    diferencias = comparar_prompts(PROMPT_V1, PROMPT_V2)

    print(diferencias)

    print("\n=== ÚLTIMA VERSIÓN ===")

    ultima = registro.ultima("pyme_copilot")

    print("Versión activa registrada:", ultima["version"])