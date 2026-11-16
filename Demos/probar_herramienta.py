from src.agente_financiero import calcular_indicadores_financieros

resultado = calcular_indicadores_financieros.invoke({
    "ingresos": 10000000,
    "costos": 5000000,
    "gastos": 2000000
})

print(resultado)