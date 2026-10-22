from src.consumir_gemini import calcular_costo

datos = {
    "usageMetadata": {
        "promptTokenCount": 850,
        "candidatesTokenCount": 320,
        "totalTokenCount": 1170
    }
}

costo = calcular_costo(
    datos,
    0.00000010,
    0.00000040
)

print(f"Costo: US$ {costo:.6f}")