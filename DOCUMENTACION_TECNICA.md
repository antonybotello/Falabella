# Documentación Técnica - Aplicación SAC Falabella (Rios del Desierto SAS)

## 1. Introducción

El presente documento detalla los aspectos técnicos de la aplicación de Sistema de Atención al Cliente (SAC) desarrollada como parte de la prueba técnica para Falabella Colombia / Rios del Desierto SAS. El sistema permite la consulta de información de clientes por número de documento y la generación de un reporte de fidelización basado en el volumen de compras.

## 2. Arquitectura General

La aplicación sigue una arquitectura web estándar con las siguientes capas principales:

* **Frontend:** Una interfaz web basada en HTML, CSS y JavaScript, servida por Django. La interactividad se logra mediante JavaScript que consume la API backend. Se utiliza Bootstrap 5 para el diseño y la presentación responsiva.
* **Backend:** Una API RESTful desarrollada con el framework Django (Python). Maneja la lógica de negocio, el procesamiento de datos y la comunicación con la base de datos.
* **Base de Datos:** SQLite se utiliza para el almacenamiento persistente de los datos de la aplicación.

## 3. Tecnologías Utilizadas

* **Lenguaje Backend:** Python (Versión 3.13.2)
* **Framework Backend:** Django (Versión Django 5.x, según `requirements.txt`)
* **Base de Datos:** SQLite 3
* **Frontend:**
    * HTML5
    * CSS3 (personalizado y a través de Bootstrap)
    * JavaScript (ECMAScript 6+)
    * Bootstrap 5 (integrado mediante `django-bootstrap5`)
* **Librerías Python Clave:**
    * `pandas`: Para la manipulación eficiente de datos y la agregación en la generación del reporte de fidelización.
    * `openpyxl`: Requerida por `pandas` para la escritura de archivos Excel en formato `.xlsx`.
    * `django-bootstrap5`: Facilita la integración de componentes y plantillas de Bootstrap 5 en Django.
    * *(Opcional: Si decidiste mantener `django-crispy-forms` y `crispy-bootstrap5`)* `django-crispy-forms` y `crispy-bootstrap5`: Configuradas para el renderizado avanzado de formularios Django con estilos Bootstrap 5.
* **Control de Versiones:** Git y GitHub.

## 4. Estructura del Proyecto

El proyecto está organizado de la siguiente manera (desde la raíz del repositorio `Falabella/`):

* `manage.py`: Script de utilidad de Django.
* `rios_desierto_project/`: Carpeta de configuración del proyecto Django.
    * `settings.py`: Archivo principal de configuración (INSTALLED_APPS, DATABASES, MIDDLEWARE, TEMPLATES, STATICFILES, etc.).
    * `urls.py`: Definiciones de URL principales del proyecto, que incluye las URLs de la aplicación `sac_app`.
    * `templates/`: Directorio para plantillas HTML base globales.
        * `base.html`: Plantilla base principal que incluye Bootstrap y la estructura común (header, footer).
        * `partials/_header.html`: Partial para la cabecera/navegación.
        * `partials/_footer.html`: Partial para el pie de página.
* `sac_app/`: Aplicación Django que contiene la lógica principal del SAC.
    * `models.py`: Definición de los modelos de datos (`TipoDocumento`, `Cliente`, `Compra`).
    * `views.py`: Contiene la lógica para las vistas, incluyendo los endpoints de la API, la generación del reporte Excel y el renderizado de la página de consulta.
    * `urls.py`: Define las rutas URL específicas para la aplicación `sac_app`.
    * `admin.py`: Configura la representación de los modelos en el panel de administración de Django.
    * `templates/sac_app/`: Contiene las plantillas HTML específicas de la aplicación `sac_app`.
        * `index.html`: Plantilla principal para la interfaz de consulta de clientes.
        * `partials/`: Contiene fragmentos de plantillas reutilizables para `index.html` (formulario, área de información del cliente, mensajes de error).
        * `reporte_mensaje.html`: Plantilla para mostrar mensajes informativos o de error relacionados con los reportes.
* `static/`: Directorio configurado en `STATICFILES_DIRS` para archivos estáticos globales del proyecto.
    * `css/style.css`: Hoja de estilos personalizada.
    * `js/scripts.js`: Archivo JavaScript principal para la lógica del frontend (llamadas a la API, manipulación del DOM, exportaciones).
    * `img/`: (Si aplica) Para imágenes como el logo.
* `db.sqlite3`: Archivo de la base de datos SQLite con el esquema y los datos de prueba.
* `requirements.txt`: Lista de todas las dependencias de Python del proyecto.
* `README.md`: Contiene la Guía de Implementación.
* `DOCUMENTACION_TECNICA.md`: Este documento.
* `.gitignore`: Especifica los archivos y directorios ignorados por Git.

## 5. Modelos de Datos

La aplicación utiliza los siguientes modelos Django:

* **`TipoDocumento`**
    * **Propósito:** Almacena los diferentes tipos de documentos de identidad.
    * **Campos Principales:**
        * `id`: PK (Autoincremental Integer).
        * `nombre_tipo`: `CharField` (Nombre completo del tipo de documento, ej. "Cédula de Ciudadanía", UNIQUE).
        * `abreviatura`: `CharField` (Abreviatura del tipo, ej. "CC", UNIQUE).

* **`Cliente`**
    * **Propósito:** Almacena la información básica de los clientes.
    * **Campos Principales:**
        * `id`: PK (Autoincremental Integer).
        * `tipo_documento`: `ForeignKey` a `TipoDocumento` (Indica el tipo de documento del cliente).
        * `numero_documento`: `CharField` (Número de documento, UNIQUE).
        * `nombre`: `CharField` (Nombres del cliente).
        * `apellido`: `CharField` (Apellidos del cliente).
        * `correo`: `EmailField` (Correo electrónico del cliente, UNIQUE).
        * `telefono`: `CharField` (Número de teléfono, opcional).
        * `fecha_registro`: `DateTimeField` (Fecha y hora del registro del cliente).

* **`Compra`**
    * **Propósito:** Almacena la información de las compras realizadas por los clientes.
    * **Campos Principales:**
        * `id`: PK (Autoincremental Integer).
        * `cliente`: `ForeignKey` a `Cliente` (Indica el cliente que realizó la compra).
        * `fecha_compra`: `DateTimeField` (Fecha y hora de la compra).
        * `monto_compra`: `DecimalField` (Monto de la compra).
        * `descripcion`: `TextField` (Descripción opcional de la compra).

## 6. API Endpoints y Vistas Clave

* **Consulta de Cliente:**
    * **Vista Django:** `sac_app.views.consultar_cliente_api`
    * **URL:** `/sac/api/cliente/consulta/<str:numero_documento>/`
    * **Método HTTP:** `GET`
    * **Parámetros URL:** `numero_documento` (string, el número de documento a consultar).
    * **Respuesta Exitosa (200 OK):** Objeto JSON con los datos del cliente: `numero_documento`, `tipo_documento` (nombre), `tipo_documento_abreviatura`, `nombre`, `apellido`, `correo`, `telefono`.
    * **Respuesta Error (404 Not Found):** Objeto JSON `{"error": "Cliente no encontrado"}`.
    * **Respuesta Error (405 Method Not Allowed):** Objeto JSON `{"error": "Método no permitido"}`.

* **Generación Reporte de Fidelización:**
    * **Vista Django:** `sac_app.views.generar_reporte_fidelizacion_excel`
    * **URL:** `/sac/reportes/fidelizacion/excel/`
    * **Método HTTP:** `GET`
    * **Respuesta Exitosa:** Descarga de un archivo Excel (`.xlsx`) que contiene: `numero_documento`, `tipo_documento` (abreviatura), `nombre_cliente`, `correo_cliente`, `telefono_cliente`, `monto_total_compras_ultimo_mes`. Solo incluye clientes cuyas compras del último mes superen los $5,000,000 COP.
    * **Respuesta Informativa/Error (HTML):** Si no hay datos que cumplan los criterios o si ocurre un error interno, se presenta una página HTML (`sac_app/reporte_mensaje.html`) con el mensaje correspondiente.

* **Página Principal de Consulta (Frontend):**
    * **Vista Django:** `sac_app.views.pagina_consulta_cliente`
    * **URL:** `/sac/`
    * **Método HTTP:** `GET`
    * **Función:** Renderiza la plantilla `sac_app/index.html`, que es la interfaz principal para el usuario.

## 7. Lógica de Negocio Principal

* **Búsqueda de Clientes:**
    1.  El usuario ingresa el tipo y número de documento en el formulario del frontend.
    2.  JavaScript (`static/js/scripts.js`) captura estos datos al hacer clic en "Buscar".
    3.  Se realiza una petición `Workspace` (GET) a la API `/sac/api/cliente/consulta/<numero_documento>/`.
    4.  La respuesta JSON de la API se utiliza para actualizar dinámicamente el DOM, mostrando la información del cliente o un mensaje de error.

* **Reporte de Fidelización:**
    1.  La vista `generar_reporte_fidelizacion_excel` calcula el "último mes" como el mes calendario completo anterior al mes actual.
    2.  Se consultan las compras (`Compra`) que caen dentro de este periodo.
    3.  Se utiliza la librería `pandas` para crear un DataFrame con estas compras y los datos relevantes del cliente.
    4.  El DataFrame se agrupa por cliente para sumar el `monto_compra`.
    5.  Se aplica un filtro para seleccionar solo aquellos clientes cuyo total de compras en el último mes es estrictamente mayor a $5,000,000 COP.
    6.  Con los clientes filtrados, se genera un archivo Excel en memoria usando `pandas` y `openpyxl`.
    7.  Este archivo Excel se devuelve como una `HttpResponse` para que el usuario lo descargue.

* **Exportación de Datos de Cliente (CSV/TXT):**
    1.  Después de una búsqueda exitosa de cliente, los datos del cliente están disponibles en JavaScript.
    2.  Al hacer clic en los botones "Exportar a CSV" o "Exportar a TXT", JavaScript formatea estos datos en el formato correspondiente.
    3.  Se crea un objeto `Blob` y se simula un clic en un enlace de descarga para que el usuario guarde el archivo `.csv` o `.txt` localmente.

## 8. Consideraciones de Diseño y Decisiones Técnicas Clave

* Se optó por **Django** debido a su robustez, el sistema ORM para una fácil interacción con la base de datos, su sistema de plantillas y su capacidad para construir APIs.
* **SQLite** fue elegido por su simplicidad y facilidad de configuración, adecuado para una prueba técnica donde no se requiere un motor de base de datos complejo.
* **Bootstrap 5**, integrado con `django-bootstrap5`, se utilizó para proporcionar un diseño responsivo y moderno rápidamente, enfocándose en la funcionalidad sobre el diseño personalizado.
* El uso de **plantillas parciales de Django** (`include` tags) ayuda a mantener el código HTML del frontend modular y organizado.
* La librería **Pandas** se seleccionó para el procesamiento de datos en el reporte de fidelización por su eficiencia y facilidad para realizar agregaciones y filtrados.
* La comunicación entre el frontend y el backend para la consulta de clientes se realiza a través de una **API RESTful simple**, devolviendo datos en formato JSON.

---