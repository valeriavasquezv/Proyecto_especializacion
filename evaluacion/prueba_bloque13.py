
from src.cliente import consultar_modelo
from prompts.banco import BANCO_DE_PROMPTS

# Recuperamos el prompt que utilizaremos
prompt = next(
    p for p in BANCO_DE_PROMPTS
    if p["nombre"] == "estructurar_receta"
)

system_instruction = prompt["system_instruction"]
response_schema = prompt["response_schema"]

# Diez preguntas diferentes
preguntas = [
    "Brownies: 250 gramos de chocolate por 2000 pesos y 100 gramos de mantequilla por 1000 pesos.",
    "Galletas: 500 gramos de harina por 800 pesos y 200 gramos de azúcar por 500 pesos.",
    "Queque: 3 huevos por 900 pesos y 250 gramos de harina por 700 pesos.",
    "Muffins: 200 gramos de harina por 600 pesos y 100 gramos de chocolate por 1200 pesos.",
    "Panqueques: 300 gramos de harina por 750 pesos y 500 ml de leche por 900 pesos.",
    "Torta: 400 gramos de harina por 1000 pesos y 200 gramos de mantequilla por 1800 pesos.",
    "Alfajores: 250 gramos de maicena por 800 pesos y 150 gramos de harina por 400 pesos.",
    "Brownies: 300 gramos de chocolate por 2500 pesos y 120 gramos de mantequilla por 1300 pesos.",
    "Queque: 200 gramos de azúcar por 500 pesos y 4 huevos por 1200 pesos.",
    "Galletas: 350 gramos de harina por 700 pesos y 150 gramos de mantequilla por 1400 pesos."
]

exitos = 0
fallidos = 0

for numero, pregunta in enumerate(preguntas, start=1):
    print(f"\n--- Consulta {numero} de 10 ---")

    try:
        respuesta = consultar_modelo(
            pregunta,
            system_instruction,
            response_schema,
        )

        print("Respuesta recibida correctamente:")
        print(respuesta)

        exitos += 1

    except (RuntimeError, ValueError, KeyError) as error:
        print(f"Consulta fallida: {error}")
        fallidos += 1

print("\n========== RESUMEN DE LA PRUEBA ==========")
print(f"Consultas exitosas: {exitos}")
print(f"Consultas fallidas: {fallidos}")
print(f"Total de consultas: {len(preguntas)}")
