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
- **Recuperación RAG:** recupera información desde una base documental utilizando ChromaDB, evalúa la relevancia de los documentos y permite consultar información respaldada por fuentes.
- **Seguridad RAG:** incorpora un filtro basado en patrones para detectar y descartar documentos que contienen instrucciones sospechosas antes de construir el contexto enviado al modelo.
- **Trazabilidad:** registra metadatos técnicos de las interacciones, evitando almacenar preguntas, respuestas y argumentos financieros en los registros de trazabilidad.
- **Supervisión humana:** incorpora mecanismos de interrupción y aprobación humana mediante HumanInTheLoopMiddleware, permitiendo controlar la ejecución de herramientas financieras y registrar las decisiones de aprobación o rechazo.

**Estado de integración:** el agente financiero incorpora supervisión humana en la ejecución de herramientas. El módulo RAG se encuentra implementado como componente separado del flujo principal del agente, con recuperación documental, evaluación de relevancia, citas y filtrado de documentos sospechosos.

### 3. Tecnologías

- Python 3.13.7
- Google Gemini API
- LangChain y LangGraph
- ChromaDB
- Pydantic
- Python-dotenv
- NumPy
- ONNX Runtime
- Pytest

### 4. Requisitos

- Python 3.13.7.
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

Instalar las dependencias:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Configurar las credenciales:

```powershell
Copy-Item .env.example .env
```

Editar el archivo `.env` y agregar la clave personal:

```dotenv
GEMINI_API_KEY=tu_clave_personal
```

No publicar ni compartir credenciales reales.

### 6. Construcción del índice documental RAG

La carpeta `vectorstore/` no se incluye en el repositorio, ya que contiene información generada localmente.

Después de instalar las dependencias y configurar la API, reconstruir el índice ejecutando desde la carpeta raíz:

```powershell
python indexar_corpus.py
```

La ejecución debe finalizar indicando que los fragmentos fueron almacenados correctamente.

El índice se guarda localmente en `vectorstore/` y utiliza ChromaDB para la recuperación documental.

**Importante:** este paso debe realizarse antes de ejecutar las demostraciones y evaluaciones que requieren recuperación RAG.

El módulo de recuperación incorpora:

- Búsqueda de documentos relevantes.
- Evaluación mediante puntajes de relevancia.
- Umbral mínimo de relevancia para evitar respuestas basadas en información insuficiente.
- Identificación de fuentes utilizadas en las respuestas.
- Detección y descarte de documentos que contienen patrones conocidos de inyección de instrucciones antes de construir el contexto enviado al modelo.

### 7. Ejecución del proyecto

Desde la carpeta raíz y con el entorno virtual activado:

```powershell
python main.py
```

La aplicación funciona mediante consola y permite probar las consultas financieras y herramientas implementadas.

Para ejecutar la demostración del agente con supervisión humana:

```powershell
python -m src.ejecutar_agente
```

Este módulo permite observar la interrupción de operaciones que requieren aprobación humana y el tratamiento de decisiones de aprobación o rechazo.

### 8. Evaluación de Gate 2

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

El ejecutor contempla las siguientes comprobaciones:

1. Recuperación documental RAG.
2. Evaluación de consultas y relevancia.
3. Privacidad y trazabilidad.
4. Supervisión humana y registro de aprobación.
5. Evidencias y resultados de evaluación.

Adicionalmente, se han realizado pruebas del filtro de seguridad RAG para verificar:

- Detección de patrones sospechosos en documentos.
- Descarte de documentos que contienen instrucciones maliciosas conocidas.
- Exclusión de documentos descartados del contexto enviado al modelo.
- Conservación de las fuentes correspondientes a los documentos legítimos.

Las pruebas de supervisión humana contemplan escenarios de aprobación y rechazo de operaciones, verificando que una operación rechazada no ejecute el cálculo financiero.

La salida completa se guarda en:

```text
entrega_gate2/resultados/ejecucion_gate2.txt
```

La carpeta también contiene evidencias documentales, métricas y registros de evaluación.

**Importante:** las pruebas de componentes y las pruebas simuladas permiten verificar comportamientos específicos, pero no sustituyen una validación integral de todos los módulos en un entorno de ejecución real.

### 9. Pruebas automatizadas

Para ejecutar las pruebas generales del proyecto:

```powershell
python -m pytest tests/ -v
```

### 10. Demostración de recuperación documental

Para probar la recuperación de documentos desde ChromaDB:

```powershell
python Demos\prueba_recuperacion.py
```

La demostración muestra los documentos recuperados, sus fuentes y los puntajes de relevancia.

### 11. Estructura principal

```text
Proyecto_especializacion/
├── main.py
├── indexar_corpus.py
├── README.md
├── requirements.txt
├── .env.example
├── src/
│   ├── agente_financiero.py
│   ├── agente_supervisado.py
│   ├── ejecutar_agente.py
│   ├── recuperacion_rag.py
│   └── trazabilidad.py
├── tests/
├── Demos/
├── evaluacion/
├── corpus/
├── docs/
└── entrega_gate2/
    ├── ejecutar_gate2.py
    ├── prueba_supervision.py
    ├── evidencias/
    └── resultados/
```

La carpeta `vectorstore/` se genera localmente al ejecutar el indexador y no se versiona en Git.

### 12. Limitaciones actuales

- Memoria conversacional sin persistencia entre reinicios.
- Funcionalidades financieras acotadas a las herramientas implementadas.
- Recuperación RAG disponible como módulo separado del flujo principal del agente.
- Filtro de inyección de instrucciones basado en patrones conocidos; no constituye una protección exhaustiva frente a todas las formas de prompt injection.
- Umbral de relevancia sujeto a evaluación y ajuste según el corpus documental.
- Supervisión humana implementada para controlar la ejecución de herramientas financieras.
- Aplicación disponible mediante consola, sin interfaz web.
- Sin conexión directa a sistemas contables empresariales.
- Requiere validación adicional en escenarios reales antes de su utilización para decisiones financieras empresariales.

### Autoría

Proyecto desarrollado en el marco de la Especialización en Desarrollo con IA Generativa de Accenture, Skillnest.

**PymeCopilot AI: Inteligencia artificial aplicada a la gestión financiera empresarial.**