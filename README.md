# PymeCopilot AI
## Agente inteligente para la gestión financiera empresarial

### 1. Descripción del proyecto

PymeCopilot AI es un prototipo de asistente financiero empresarial desarrollado como proyecto integrador de la Especialización en Desarrollo con IA Generativa de Accenture.

Su objetivo es apoyar a pequeñas y medianas empresas (PYMEs) en la comprensión y análisis de información financiera, facilitando el acceso a cálculos, indicadores y explicaciones que contribuyan a una mejor toma de decisiones.

El proyecto utiliza inteligencia artificial generativa mediante Google Gemini, junto con herramientas financieras deterministas desarrolladas en Python y mecanismos de orquestación con LangChain.

La solución busca evolucionar hacia una plataforma integral de inteligencia empresarial con IA, orientada a PYMEs y empresas medianas.

### 2. Objetivos

- Facilitar la comprensión de conceptos financieros empresariales.
- Automatizar cálculos básicos de rentabilidad.
- Interpretar consultas financieras mediante un agente inteligente.
- Incorporar herramientas especializadas para resolver solicitudes.
- Mantener memoria conversacional por sesión.
- Registrar las interacciones y herramientas utilizadas para facilitar la trazabilidad.

### 3. Funcionalidades implementadas

**3.1. Agente financiero inteligente**

Agente desarrollado con LangChain y conectado a Google Gemini.

Permite interpretar consultas financieras, generar explicaciones y decidir cuándo utilizar las herramientas disponibles.

**3.2. Cálculo de indicadores financieros**

Herramienta determinista que recibe ingresos, costos y gastos, y calcula:

- Utilidad.
- Margen de utilidad.
- Porcentaje de costos sobre ingresos.
- Porcentaje de gastos sobre ingresos.

**3.3. Consulta de conceptos financieros**

Herramienta de consulta de definiciones para los siguientes conceptos:

- Liquidez.
- EBITDA.
- Capital de trabajo.
- Punto de equilibrio.
- Margen de utilidad.

**3.4. Memoria conversacional**

Implementación de memoria independiente por identificador de sesión, permitiendo mantener el contexto de las conversaciones durante la ejecución del programa.

La memoria actual se mantiene en memoria RAM y no tiene persistencia entre reinicios.

**3.5. Enrutamiento de solicitudes**

Módulo complementario que clasifica las solicitudes financieras en tres categorías:

- Consulta.
- Problema.
- Mejora.

Cada categoría dispone de una cadena especializada de procesamiento.

Este módulo se encuentra desarrollado de forma independiente y no está integrado todavía en el flujo principal del agente.

**3.6. Trazabilidad**

Registro de las interacciones en formato JSONL, incluyendo:

- Fecha y hora.
- Identificador de sesión.
- Consulta del usuario.
- Herramientas utilizadas.
- Argumentos entregados a las herramientas.
- Resultados obtenidos.
- Respuesta final del agente.

**3.7. Manejo de errores y reintentos**

El proyecto incorpora mecanismos para gestionar errores de conexión, respuestas de la API y reintentos ante fallos temporales.

### 4. Tecnologías utilizadas

- Python 3.11.
- Google Gemini API.
- LangChain.
- LangChain Classic.
- LangGraph.
- Pydantic.
- Requests.
- Python-dotenv.
- Pytest.

### 5. Arquitectura general

El proyecto utiliza una arquitectura modular que separa la ejecución del agente, las herramientas financieras y la trazabilidad.

Flujo principal:

1. El usuario ingresa una consulta.
2. El punto de entrada inicializa el modelo Gemini.
3. Se construye el agente financiero.
4. El agente interpreta la solicitud.
5. Si corresponde, utiliza una herramienta financiera.
6. Se genera la respuesta.
7. Se registra la interacción en el archivo de trazabilidad.

### 6. Requisitos previos

Para ejecutar el proyecto se necesita:

- Python 3.11.
- Git.
- Conexión a internet.
- Una clave válida de Google Gemini API, obtenida desde [Google AI Studio](https://aistudio.google.com/app/apikey).

### 7. Instalación

Clonar el repositorio:

```powershell
git clone https://github.com/valeriavasquezv/Proyecto_especializacion.git
cd Proyecto_especializacion
```

Crear un entorno virtual:

```powershell
python -m venv .venv
```

Activar el entorno virtual en Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Actualizar pip e instalar las dependencias:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 8. Configuración de credenciales

Crear el archivo `.env` a partir de la plantilla:

```powershell
Copy-Item .env.example .env
```

Configurar la clave de Gemini dentro del archivo `.env`:

```dotenv
GEMINI_API_KEY=tu_clave_personal
```

No se deben publicar ni compartir credenciales reales.

El archivo `.env` debe permanecer excluido del control de versiones mediante `.gitignore`.

### 9. Ejecución

Desde la carpeta raíz del proyecto, ejecutar:

```powershell
python main.py
```

La versión actual ejecuta consultas de demostración que permiten comprobar:

- La capacidad del agente para responder consultas generales sobre gestión financiera.
- La utilización de la herramienta de cálculo de indicadores financieros.
- La generación de respuestas y el registro de las herramientas utilizadas.

La aplicación funciona actualmente mediante consola. No dispone todavía de una interfaz web.

### 10. Pruebas automatizadas

El proyecto cuenta con pruebas automatizadas utilizando Pytest.

Para ejecutarlas:

```powershell
python -m pytest tests/ -v
```

**Resultado de validación local:**

- 20 pruebas ejecutadas.
- 20 pruebas aprobadas.
- Tiempo de ejecución registrado: 3,30 segundos.

Las pruebas abarcan cadenas, cliente Gemini, reintentos, enrutamiento, manejo de errores y procesamiento de texto.

### 11. Estructura del proyecto

```text
Proyecto_especializacion/
│
├── main.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── src/
│   ├── agente_financiero.py
│   ├── ejecutar_agente.py
│   ├── trazabilidad.py
│   ├── enrutamiento.py
│   ├── cadena_tres_pasos.py
│   └── módulos de integración y soporte
│
├── tests/
│   └── pruebas automatizadas
│
├── demos/
│   └── demostraciones de funcionalidades
│
├── evaluacion/
│   ├── datos/
│   └── resultados/
│
├── prompts/
│
└── docs/
    └── documentación técnica
```

### 12. Limitaciones actuales

La versión actual corresponde a un prototipo funcional y presenta las siguientes limitaciones:

- La memoria conversacional no tiene persistencia.
- Los cálculos financieros están limitados a los indicadores implementados.
- Las definiciones financieras están disponibles mediante un conjunto acotado de conceptos.
- El módulo de enrutamiento todavía no está integrado en el flujo principal.
- La ejecución se realiza mediante consola.
- No existe todavía conexión con sistemas contables o bases de datos empresariales.

### 13. Evolución futura

La visión de PymeCopilot AI es evolucionar hacia una plataforma de inteligencia empresarial con IA, que permita a las organizaciones comprender su situación financiera, anticipar riesgos y apoyar sus decisiones.

Entre las funcionalidades futuras se consideran:

- Análisis de liquidez y flujo de caja.
- Análisis de capital de trabajo.
- Evaluación de costos y rentabilidad.
- Proyecciones financieras.
- Presupuestos y análisis de desviaciones.
- Detección de riesgos financieros.
- Integración de datos desde sistemas empresariales.
- Memoria persistente por empresa.
- Interfaz web y paneles de indicadores.

Estas funcionalidades corresponden a objetivos de desarrollo futuro y no forman parte de la implementación actual.

### 14. Seguridad y buenas prácticas

- Mantener las credenciales fuera del código fuente.
- No publicar archivos `.env`.
- Utilizar entornos virtuales.
- Mantener las dependencias declaradas en `requirements.txt`.
- Ejecutar las pruebas automatizadas después de realizar cambios.
- Evitar publicar archivos de trazabilidad que puedan contener información sensible.

### 15. Autoría y contexto académico

Proyecto desarrollado en el marco de la Especialización en Desarrollo con IA Generativa de Accenture, Skillnest.

**PymeCopilot AI: Inteligencia artificial aplicada a la gestión financiera empresarial.**

