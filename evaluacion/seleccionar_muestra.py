
import json

with open("resultados_metricas.json", "r", encoding="utf-8") as archivo:
    resultados = json.load(archivo)

casos_ordenados = sorted(resultados, key=lambda caso: caso["f1"])

peores_casos = casos_ordenados[:5]
mejores_casos = casos_ordenados[-5:]

print("\n===== 5 CASOS CON MENOR F1 =====")

for caso in peores_casos:
    print(f"F1: {caso['f1']:.4f} | {caso['consulta']}")

print("\n===== 5 CASOS CON MAYOR F1 =====")

for caso in mejores_casos:
    print(f"F1: {caso['f1']:.4f} | {caso['consulta']}")

muestra_revision = peores_casos + mejores_casos

with open("muestra_revision.json", "w", encoding="utf-8") as archivo:
    json.dump(muestra_revision, archivo, indent=2, ensure_ascii=False)

print("\nArchivo muestra_revision.json creado correctamente.")