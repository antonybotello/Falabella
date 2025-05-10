document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const formConsultaCliente = document.getElementById('formConsultaCliente');
    const infoClienteDiv = document.getElementById('infoCliente'); 
    const mensajeErrorDiv = document.getElementById('mensajeError'); 

    // Spans dentro de infoClienteDiv para mostrar los datos específicos
    const clienteTipoDocSpan = document.getElementById('clienteTipoDoc');
    const clienteTipoDocAbrSpan = document.getElementById('clienteTipoDocAbr');
    const clienteNumDocSpan = document.getElementById('clienteNumDoc');
    const clienteNombreSpan = document.getElementById('clienteNombre');
    const clienteApellidoSpan = document.getElementById('clienteApellido');
    const clienteCorreoSpan = document.getElementById('clienteCorreo');
    const clienteTelefonoSpan = document.getElementById('clienteTelefono');

    // Botones de exportación
    const btnExportarCSV = document.getElementById('btnExportarCSV');
    const btnExportarTXT = document.getElementById('btnExportarTXT');
    // Si añades un botón para exportar Excel individual, obténlo aquí también:
    // const btnExportarExcelIndividual = document.getElementById('btnExportarExcelIndividual');

    let datosClienteActual = null; // Variable para almacenar los datos del cliente actualmente consultado

    // Event listener para el envío del formulario de consulta
    if (formConsultaCliente) {
        formConsultaCliente.addEventListener('submit', function(event) {
            event.preventDefault(); // Evita el envío tradicional del formulario

            const numeroDocumentoInput = document.getElementById('numeroDocumento');
            const numeroDocumento = numeroDocumentoInput.value.trim();

            if (!numeroDocumento) {
                mostrarError("Por favor, ingrese el número de documento.");
                numeroDocumentoInput.focus(); // Poner foco en el input
                return;
            }

            // Limpiar resultados y errores anteriores
            ocultarInfoCliente();
            ocultarError();

            // Construir la URL de la API
            // Asume que el prefijo de la app SAC en urls.py del proyecto es '/sac/'
            const apiUrl = `/sac/api/cliente/consulta/${encodeURIComponent(numeroDocumento)}/`;

            // Realizar la petición fetch a la API
            fetch(apiUrl)
                .then(response => {
                    if (response.status === 404) {
                        throw new Error("Cliente no encontrado.");
                    }
                    if (!response.ok) {
                        // Intenta obtener un mensaje de error del cuerpo JSON si existe
                        return response.json().then(errData => {
                            throw new Error(errData.error || `Error del servidor: ${response.status}`);
                        }).catch(() => { // Si el cuerpo del error no es JSON o está vacío
                            throw new Error(`Error del servidor: ${response.status}`);
                        });
                    }
                    return response.json(); // Convertir la respuesta a JSON
                })
                .then(data => {
                    datosClienteActual = data; // Guardar los datos para las funciones de exportación
                    mostrarInfoCliente(data);
                })
                .catch(error => {
                    datosClienteActual = null; // Limpiar datos en caso de error
                    mostrarError(error.message);
                });
        });
    }

    // Funciones auxiliares para mostrar/ocultar información y errores
    function mostrarInfoCliente(data) {
        if (!infoClienteDiv) return; // Seguridad por si el elemento no existe

        clienteTipoDocSpan.textContent = data.tipo_documento || 'N/A';
        clienteTipoDocAbrSpan.textContent = data.tipo_documento_abreviatura || 'N/A';
        clienteNumDocSpan.textContent = data.numero_documento || 'N/A';
        clienteNombreSpan.textContent = data.nombre || 'N/A';
        clienteApellidoSpan.textContent = data.apellido || 'N/A';
        clienteCorreoSpan.textContent = data.correo || 'N/A';
        clienteTelefonoSpan.textContent = data.telefono || 'N/A';
        
        infoClienteDiv.classList.remove('d-none'); // Usa 'd-none' de Bootstrap para mostrar
        ocultarError(); // Ocultar cualquier mensaje de error previo
    }

    function ocultarInfoCliente() {
        if (infoClienteDiv) {
            infoClienteDiv.classList.add('d-none'); // Usa 'd-none' de Bootstrap para ocultar
        }
        datosClienteActual = null; // Limpiar los datos guardados
    }

    function mostrarError(mensaje) {
        if (!mensajeErrorDiv) return; // Seguridad

        mensajeErrorDiv.textContent = mensaje;
        mensajeErrorDiv.classList.remove('d-none'); // Usa 'd-none' de Bootstrap para mostrar
        ocultarInfoCliente(); // Ocultar cualquier información de cliente previa
    }

    function ocultarError() {
        if (mensajeErrorDiv) {
            mensajeErrorDiv.classList.add('d-none'); // Usa 'd-none' de Bootstrap para ocultar
        }
    }

    // --- Funcionalidad de Exportación para el cliente consultado ---
    if (btnExportarCSV) {
        btnExportarCSV.addEventListener('click', function() {
            if (datosClienteActual) {
                exportarAFormato(datosClienteActual, 'csv');
            } else {
                alert("Primero debe buscar y encontrar un cliente para poder exportar sus datos.");
            }
        });
    }

    if (btnExportarTXT) {
        btnExportarTXT.addEventListener('click', function() {
            if (datosClienteActual) {
                exportarAFormato(datosClienteActual, 'txt');
            } else {
                alert("Primero debe buscar y encontrar un cliente para poder exportar sus datos.");
            }
        });
    }

    function exportarAFormato(data, formato) {
        if (!data) {
            console.error("No hay datos de cliente para exportar.");
            return;
        }

        let contenido = '';
        const nombreArchivoBase = `cliente_${data.numero_documento || 'desconocido'}`;
        let mimeType = '';
        let extension = formato;

        // Preparar el contenido basado en el formato
        if (formato === 'csv') {
            contenido = "Campo,Valor\n"; // Encabezados CSV
            contenido += `Tipo Documento,"${data.tipo_documento || ''} (${data.tipo_documento_abreviatura || ''})"\n`;
            contenido += `Numero Documento,"${data.numero_documento || ''}"\n`;
            contenido += `Nombre,"${data.nombre || ''}"\n`;
            contenido += `Apellido,"${data.apellido || ''}"\n`;
            contenido += `Correo,"${data.correo || ''}"\n`;
            contenido += `Telefono,"${data.telefono || ''}"\n`;
            // Puedes añadir más campos si los tienes en 'data'
            mimeType = 'text/csv';
        } else if (formato === 'txt') {
            contenido = "Información del Cliente:\n";
            contenido += "-------------------------\n";
            contenido += `Tipo Documento: ${data.tipo_documento || ''} (${data.tipo_documento_abreviatura || ''})\n`;
            contenido += `Numero Documento: ${data.numero_documento || ''}\n`;
            contenido += `Nombre: ${data.nombre || ''}\n`;
            contenido += `Apellido: ${data.apellido || ''}\n`;
            contenido += `Correo: ${data.correo || ''}\n`;
            contenido += `Telefono: ${data.telefono || ''}\n`;
            // Puedes añadir más campos si los tienes en 'data'
            mimeType = 'text/plain';
        } else {
            console.error("Formato de exportación no soportado:", formato);
            return;
        }

        // Crear Blob y enlace de descarga
        const blob = new Blob([contenido], { type: `${mimeType};charset=utf-8;` });
        const link = document.createElement("a");

        // Feature detection para compatibilidad de descarga
        if (link.download !== undefined) {
            const url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", `${nombreArchivoBase}.${extension}`);
            link.style.visibility = 'hidden'; // Hacer el enlace invisible
            document.body.appendChild(link); // Añadir el enlace al DOM para que funcione en Firefox
            link.click(); // Simular clic en el enlace
            document.body.removeChild(link); // Quitar el enlace del DOM
            URL.revokeObjectURL(url); // Liberar el objeto URL
        } else {
            // Fallback para navegadores que no soportan el atributo 'download'
            alert("La descarga directa no es soportada por su navegador. Por favor, copie el contenido manualmente.");
        }
    }

});