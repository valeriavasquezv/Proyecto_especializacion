
from src.cliente_reintento import con_reintento

intentos_previos = 0


def operacion_simulada():
    global intentos_previos
    intentos_previos += 1

    if intentos_previos < 3:
        raise TimeoutError(
            "Límite de peticiones excedido."
        )

    return {
        "contenido": "Respuesta simulada exitosa",
        "intento": intentos_previos,
    }


respuesta = con_reintento(
    operacion_simulada,
    intentos=3,
    espera_base=2,
)

print(respuesta)
