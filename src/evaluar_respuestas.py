
from src.pipeline_texto import procesar_texto


# ==========================================
# FUNCIONES REUTILIZABLES
# ==========================================

def calcular_coincidencia(referencia, respuesta):
    palabras_referencia = set(referencia)
    palabras_respuesta = set(respuesta)

    palabras_comunes = palabras_referencia & palabras_respuesta

    if not palabras_referencia:
        return 0, palabras_comunes

    porcentaje = (
        len(palabras_comunes) / len(palabras_referencia)
    ) * 100

    return porcentaje, palabras_comunes


def evaluar_caso(nombre, referencia, respuesta):

    # Comparación sin procesar
    tokens_ref_crudo = referencia.split()
    tokens_resp_crudo = respuesta.split()

    pct_crudo, comunes_crudo = calcular_coincidencia(
        tokens_ref_crudo,
        tokens_resp_crudo
    )

    # Comparación después del pipeline
    tokens_ref = procesar_texto(referencia)
    tokens_resp = procesar_texto(respuesta)

    pct_procesado, comunes = calcular_coincidencia(
        tokens_ref,
        tokens_resp
    )

    # Mostrar resultados
    print(f"\n=== EVALUACIÓN DE {nombre.upper()} ===")

    print("\nCoincidencia sin procesar:")
    print(f"{pct_crudo:.1f}%")

    print("\nCoincidencia después del pipeline:")
    print(f"{pct_procesado:.1f}%")

    print("\nPalabras coincidentes:")
    print(comunes)


# ==========================================
# CASO 1: VENTAS
# ==========================================

referencia = """
Para aumentar las ventas de una pastelería pequeña,
se recomienda implementar un programa de fidelización,
publicar contenido en redes sociales y crear combos
promocionales para aumentar el ticket promedio.
"""

respuesta = """
Aquí tienes tres acciones concretas para aumentar las ventas de una pastelería pequeña:

1. Implementar un programa de lealtad: Ofrece una tarjeta de compra 10 y obtén 1 gratis para incentivar la recurrencia de los clientes locales.
2. Optimizar la presencia en redes sociales: Publica fotos y videos cortos de alta calidad mostrando tus productos.
3. Crear combos de ocasión especial: Diseña paquetes promocionales para aumentar el ticket promedio de compra por cliente.
"""


# ==========================================
# CASO 2: COSTOS
# ==========================================

referencia_costos = """
Para calcular el costo de producción de una torta,
primero se deben calcular los ingredientes y materiales
utilizados en la receta. Luego se deben considerar los
costos indirectos como electricidad, gas y agua.
Finalmente se debe calcular la mano de obra y sumar
todos los componentes para obtener el costo total.
"""

respuesta_costos = """
Aquí tienes tres pasos fundamentales para calcular el costo de producción de una torta:

1. Listar y costear insumos: Identifica todos los ingredientes utilizados y calcula el costo exacto de la cantidad empleada en la receta, incluyendo los insumos de empaque.

2. Determinar los costos indirectos: Calcula una proporción de los gastos fijos mensuales como gas, electricidad, agua, alquiler y servicios de internet.

3. Sumar la mano de obra: Asigna un valor monetario al tiempo dedicado a la preparación, horneado y decoración.

La suma de estos tres componentes dará el costo total de producción.
"""


# ==========================================
# CASO 3: INVENTARIO
# ==========================================

referencia_inventario = """
Para evitar pérdidas por vencimiento en una pastelería,
se debe aplicar el método PEPS para utilizar primero
los ingredientes más antiguos. También se debe mantener
un registro actualizado del inventario y las fechas
de vencimiento. Finalmente, se deben estandarizar
las recetas y planificar la producción según la demanda
para reducir desperdicios.
"""

respuesta_inventario = """
Aquí tienes tres acciones efectivas para evitar pérdidas en tu pastelería:

1. Implementar el sistema PEPS (Primero en Entrar, Primero en Salir): Organiza tus estantes colocando los productos nuevos detrás de los antiguos, asegurándote de usar siempre primero los que tienen una fecha de vencimiento más próxima.

2. Gestionar un inventario digital o físico actualizado: Lleva un control riguroso de tus existencias y fechas de caducidad para planificar compras basadas en la rotación real.

3. Estandarizar recetas y porciones: Utiliza fichas técnicas exactas para evitar el desperdicio durante la preparación y ajusta el volumen de producción según la demanda real.
"""


# ==========================================
# EJECUTAR EVALUACIONES
# ==========================================

if __name__ == "__main__":

    evaluar_caso("Ventas", referencia, respuesta)

    evaluar_caso("Costos", referencia_costos, respuesta_costos)

    evaluar_caso("Inventario", referencia_inventario, respuesta_inventario)
