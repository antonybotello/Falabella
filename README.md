# Guía de Implementación - Aplicación SAC Falabella (Rios del Desierto SAS)

## 1. Introducción

Esta guía describe los pasos necesarios para configurar y ejecutar la aplicación de Sistema de Atención al Cliente (SAC) desarrollada como parte de la prueba técnica para Falabella Colombia / Rios del Desierto SAS. La aplicación permite consultar información de clientes por su número de documento y generar reportes de fidelización.

## 2. Requisitos Previos

Antes de comenzar, asegúrese de tener instalado el siguiente software en su sistema:

* **Python:** Versión 3.13.2 (la aplicación fue desarrollada con esta versión). Se recomienda usar Python 3.12 o superior.
* **pip:** El gestor de paquetes de Python (usualmente se instala con Python).
* **Git:** Para clonar el repositorio del proyecto.
* **Navegador Web Moderno:** Para acceder a la aplicación (ej. Chrome, Firefox, Edge).

## 3. Pasos de Instalación y Configuración

Siga estos pasos para poner en funcionamiento la aplicación en un entorno local:

**3.1. Obtener el Código Fuente**

* Abra una terminal o línea de comandos y ejecute:
    ```bash
    git clone https://github.com/antonybotello/Falabella.git
    ```

**3.2. Navegar al Directorio del Proyecto**
    En la terminal, navegue hasta la carpeta raíz del proyecto que se acaba de clonar:
    ```bash
    cd Falabella
    ```
    (Dentro de esta carpeta `Falabella` es donde se encontrará el archivo `manage.py`).

**3.3. Crear y Activar un Entorno Virtual**
    Es una buena práctica aislar las dependencias del proyecto. Desde la carpeta `Falabella`:
    ```bash
    python -m venv venv
    ```
    Para activar el entorno virtual:
    * **En Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **En macOS o Linux:**
        ```bash
        source venv/bin/activate
        ```
    Debería ver `(venv)` al inicio de la línea de su terminal, indicando que el entorno virtual está activo.

**3.4. Instalar Dependencias**
    Con el entorno virtual activado, instale todas las librerías necesarias ejecutando:
    ```bash
    pip install -r requirements.txt
    ```
    Este comando leerá el archivo `requirements.txt` (ubicado en la carpeta `Falabella`) e instalará Django, Pandas, openpyxl, django-bootstrap5 y otras dependencias.

**3.5. Configuración de la Base de Datos**
    * El proyecto utiliza una base de datos SQLite3.
    * El archivo de base de datos `db.sqlite3` se incluye en el repositorio y ya contiene la estructura de tablas necesaria y los datos de prueba (3 tipos de documento, 10 clientes y sus compras, con el cliente "Ana Pérez" cumpliendo los criterios para el reporte de fidelización de Abril 2025).
    * **No es necesario ejecutar `python manage.py migrate`** si se utiliza el archivo `db.sqlite3` proporcionado, ya que el esquema y los datos ya están implementados.

**3.6. Credenciales de Superusuario para el Panel de Administración de Django (Opcional)**
    Si desea explorar los datos directamente en el panel de administración de Django (`/admin/`), puede utilizar las siguientes credenciales (ya creadas en la base de datos proporcionada):
    * **Usuario:** `admin`
    * **Contraseña:** `@dmin1234`
    Si por alguna razón estas credenciales no funcionaran o deseara crear otro superusuario, puede hacerlo con el comando (asegúrese de que el entorno virtual esté activado):


    python manage.py createsuperuser
    

  Y siga las instrucciones en pantalla.

## 4. Ejecución de la Aplicación

Una vez completados los pasos de instalación y configuración:

1.  Asegúrese de que su entorno virtual (`venv`) esté activo.
2.  En la terminal, desde la carpeta raíz del proyecto (`Falabella`, donde se encuentra `manage.py`), ejecute el servidor de desarrollo de Django:
    ```bash
    python manage.py runserver
    ```
3.  Verá un mensaje indicando que el servidor se está ejecutando, usualmente en `http://127.0.0.1:8000/`.

4.  **Acceder a la Aplicación:**
    Abra su navegador web y diríjase a la siguiente URL para acceder a la interfaz principal de la aplicación SAC:
    ```
    http://127.0.0.1:8000/sac/
    ```

    Desde allí podrá:
    * Buscar clientes por su número de documento.
    * Ver la información del cliente encontrado.
    * Exportar los datos del cliente a CSV o TXT.
    * Descargar el reporte de fidelización en formato Excel.

## 5. Notas Adicionales

* La aplicación ha sido desarrollada y probada en un entorno de desarrollo con `DEBUG = True` (configurado en `rios_desierto_project/settings.py`).
* No se requieren variables de entorno específicas para esta implementación básica.

---
