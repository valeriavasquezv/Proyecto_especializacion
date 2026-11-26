# PymeCopilot AI
## Agente inteligente para la gestión financiera empresarial

### 1. Descripción

PymeCopilot AI es un prototipo de asistente financiero empresarial desarrollado como proyecto integrador de la Especialización en Desarrollo con IA Generativa de Accenture.

Utiliza Google Gemini, Python y herramientas financieras deterministas para interpretar consultas, calcular indicadores y entregar explicaciones que apoyen la toma de decisiones en PYMEs.

### 2. Funcionalidades

- **Agente financiero:** interpreta consultas y utiliza herramientas según la solicitud.
- **Indicadores financieros:** calcula utilidad, margen de utilidad y porcentajes de costos y gastos.
- **Conceptos financieros:** permite consultar definiciones como EBITDA, liquidez y capital de trabajo.
- **Memoria conversacional:** mantiene contexto por sesión durante la ejecución.
- **Manejo de errores:** incorpora mecanismos de reintento ante fallos temporales.
- **Recuperación RAG:** módulo experimental de recuperación de información documental.
- **Trazabilidad:** registra metadatos técnicos sin almacenar preguntas, respuestas ni argumentos financieros.
- **Supervisión humana:** módulo independiente que permite interrumpir un flujo, solicitar aprobación y registrar su resultado.

Algunos módulos complementarios, como el enrutamiento, RAG y supervisión humana, todavía no están integrados completamente en el flujo principal del agente.

### 3. Tecnologías

- Python 3.11
- Google Gemini API
- LangChain y LangGraph
- ChromaDB
- Pydantic
- Python-dotenv
- Pytest

### 4. Requisitos

- Python 3.11.
- Git.
- Conexión a internet.
- Clave de Google Gemini API: [Google AI Studio](https://aistudio.google.com/app/apikey).

### 5. Instalación y configuración

Clonar el repositorio:

```powershell
git clone https://github.com/valeriavasquezv/Proyecto_especializacion.git
cd Proyecto_especializacion
```

Crear y activar el entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Configurar las credenciales:

```powershell
Copy-Item .env.example .env
```

Editar `.env` y agregar:

```dotenv
GEMINI_API_KEY=tu_clave_personal
```

No publicar ni compartir credenciales reales.

### 6. Ejecución del proyecto

Desde la carpeta raíz:

```powershell
python main.py
```

La aplicación funciona mediante consola y permite probar las consultas financieras y herramientas implementadas.

### 7. Evaluación de Gate 2

Se dispone de una carpeta específica para facilitar la revisión académica:

```text
entrega_gate2/
├── ejecutar_gate2.py
├── prueba_supervision.py
├── evidencias/
└── resultados/
```

Para ejecutar las pruebas de Gate 2:

```powershell
python entrega_gate2\ejecutar_gate2.py
```

El ejecutor realiza las siguientes comprobaciones:

1. Recuperación documental RAG.
2. Evaluación de consultas y relevancia.
3. Privacidad y trazabilidad.
4. Supervisión humana y registro de aprobación.

La salida completa se guarda en:

```text
entrega_gate2/resultados/ejecucion_gate2.txt
```

La carpeta también contiene evidencias documentales, métricas y registros de evaluación.

**Importante:** estas pruebas validan módulos de manera independiente. Su aprobación no implica que todos estén integrados en el flujo principal del agente.

### 8. Pruebas automatizadas

Para ejecutar las pruebas generales del proyecto:

```powershell
python -m pytest tests/ -v
```

### Estructura principal

```text
Proyecto_especializacion/
├── main.py
├── README.md
├── requirements.txt
├── .env.example
├── src/
├── tests/
├── Demos/
├── evaluacion/
├── corpus/
├── vectorstore/
├── docs/
└── entrega_gate2/
```

### Limitaciones actuales

- Memoria conversacional sin persistencia entre reinicios.
- Funcionalidades financieras acotadas a las herramientas implementadas.
- Módulos complementarios todavía no integrados completamente.
- Recuperación RAG experimental, con precisión documental por mejorar.
- Aplicación disponible mediante consola, sin interfaz web.
- Sin conexión directa a sistemas contables empresariales.

### Autoría

Proyecto desarrollado en el marco de la Especialización en Desarrollo con IA Generativa de Accenture, Skillnest.

**PymeCopilot AI: Inteligencia artificial aplicada a la gestión financiera empresarial.**