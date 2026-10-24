# Miniaplicación de IA Generativa para estructurar información de recetas

## 1. Descripción del proyecto

Este proyecto forma parte de la Especialización en Desarrollo con IA Generativa de Accenture.

La miniaplicación utiliza la API de Gemini para procesar información textual relacionada con recetas e ingredientes y organizarla en estructuras JSON. Permite extraer datos de productos, identificar información faltante y estructurar los ingredientes con sus cantidades, unidades y precios cuando están disponibles.

El proyecto constituye una primera etapa técnica de una solución orientada a apoyar la gestión de pequeñas y medianas empresas (PYMEs).

### Visión futura

La visión del proyecto es evolucionar hacia un ayudante financiero para PYMEs que facilite la gestión de costos y precios de venta. Entre sus posibles funcionalidades futuras se encuentran el cálculo de costos unitarios, la estimación de precios según márgenes deseados, el análisis de rentabilidad y el cálculo del punto de equilibrio.

Estas funcionalidades forman parte de la evolución prevista y no se consideran implementadas en la versión actual.

## 2. Funcionalidades actuales

- Consumo de la API de Gemini mediante peticiones HTTP.
- Uso de instrucciones de sistema y esquemas para orientar las respuestas estructuradas.
- Extracción y organización de información de recetas e ingredientes.
- Identificación de datos faltantes en la información recibida.
- Procesamiento de respuestas JSON.
- Pruebas de consistencia del banco de prompts.
- Gestión de credenciales mediante variables de entorno.

## 3. Tecnologías utilizadas

- Python.
- API de Google Gemini.
- `requests` para las peticiones HTTP.
- `python-dotenv` para cargar variables de entorno.
- `json` para procesar las respuestas estructuradas.

## 4. Requisitos previos

Para instalar y ejecutar el proyecto se necesita:

- Python instalado.
- Git instalado.
- Una clave válida de la API de Gemini, obtenida desde [Google AI Studio](https://aistudio.google.com/app/apikey).

## 5. Instalación

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

Instalar las dependencias:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 6. Configuración de credenciales

Crear un archivo `.env` a partir de la plantilla:

```powershell
Copy-Item .env.example .env
```

Abrir `.env` y configurar una clave propia de Gemini:

```dotenv
GEMINI_API_KEY=tu_clave_personal
```

Reemplazar `tu_clave_personal` por una clave válida. No se deben compartir ni publicar credenciales reales.

El archivo `.env` está excluido del control de versiones mediante `.gitignore`. El archivo `.env.example` debe contener únicamente valores de ejemplo.

## 7. Ejecución de la miniaplicación

Desde la carpeta raíz del proyecto, ejecutar:

```powershell
python main.py
```

La aplicación envía una consulta a Gemini para estructurar información de una receta y muestra el resultado en formato JSON.

La salida incluye el producto y sus ingredientes, con los nombres, cantidades, unidades y precios disponibles en la información procesada.

La ejecución requiere conexión a internet y una clave válida de Gemini. La disponibilidad del servicio puede afectar temporalmente las solicitudes.

## 8. Banco y pruebas de consistencia de prompts

El directorio `prompts/` contiene el banco de prompts y el script de pruebas de consistencia.

Para ejecutar las pruebas:

```powershell
python prompts/test_consistencia.py
```

El script realiza solicitudes a la API, evalúa las respuestas y registra los resultados en `prompts/registro_resultados.json`.

Las pruebas requieren una clave válida de Gemini. Los errores temporales del servicio, como las respuestas HTTP 503, pueden afectar los resultados.

## 9. Estructura del repositorio

- `main.py`: punto de entrada de la miniaplicación.
- `src/consumir_gemini.py`: funciones para preparar peticiones, enviar solicitudes a Gemini y procesar las respuestas.
- `prompts/banco.py`: banco de prompts y esquemas de respuesta.
- `prompts/test_consistencia.py`: pruebas de consistencia de los prompts.
- `prompts/registro_resultados.json`: registro de resultados de las pruebas.
- `docs/`: documentación técnica, decisiones de arquitectura, diagramas y evidencias.
- `tests/`: directorio destinado a las pruebas del proyecto.
- `requirements.txt`: dependencias de Python.
- `.env.example`: plantilla de configuración de credenciales.
- `.gitignore`: archivos y directorios excluidos del control de versiones.

## 10. Seguridad y buenas prácticas

- No escribir claves de API, contraseñas ni tokens directamente en el código.
- No subir el archivo `.env` al repositorio.
- Mantener `.env.example` libre de credenciales reales.
- Utilizar un entorno virtual propio para el proyecto.
- Registrar los cambios mediante commits en Git.

## 11. Evolución del proyecto

El proyecto se ampliará progresivamente durante los siguientes bloques de la especialización.

La evolución prevista es convertir la miniaplicación en un ayudante financiero para PYMEs, incorporando gradualmente herramientas para calcular costos, apoyar la definición de precios de venta y analizar la rentabilidad de productos.

La incorporación de estas funcionalidades dependerá de los requisitos y objetivos de los siguientes hitos del programa.

