document.addEventListener('DOMContentLoaded', function() {
    const formConsultaCliente = document.getElementById('formConsultaCliente');
    const infoClienteDiv = document.getElementById('infoCliente');
    const mensajeErrorDiv = document.getElementById('mensajeError');

    const clienteTipoDocSpan = document.getElementById('clienteTipoDoc');
    const clienteTipoDocAbrSpan = document.getElementById('clienteTipoDocAbr');
    const clienteNumDocSpan = document.getElementById('clienteNumDoc');
    const clienteNombreSpan = document.getElementById('clienteNombre');
    const clienteApellidoSpan = document.getElementById('clienteApellido');
    const clienteCorreoSpan = document.getElementById('clienteCorreo');
    const clienteTelefonoSpan = document.getElementById('clienteTelefono');

    const btnExportarCSV = document.getElementById('btnExportarCSV');
    const btnExportarTXT = document.getElementById('btnExportarTXT');

    let datosClienteActual = null; // Almacena los datos del cliente actualmente consultado

    if (formConsultaCliente) {
        formConsultaCliente.addEventListener('submit', function(event) {
            event.preventDefault();

            ocultarInfoCliente();
            ocultarError();

            const numeroDocumentoInput = document.getElementById('numeroDocumento');
            const numeroDocumento = numeroDocumentoInput.value.trim();

            if (!numeroDocumento) {
                mostrarError("Por favor, ingrese el número de documento.");
                if (numeroDocumentoInput) numeroDocumentoInput.focus();
                return;
            }
            
            const apiUrl = `/sac/api/cliente/consulta/${encodeURIComponent(numeroDocumento)}/`;

            fetch(apiUrl)
                .then(response => {
                    if (response.status === 404) {
                        throw new Error("Cliente no encontrado.");
                    }
                    if (!response.ok) {
                        return response.json().then(errData => {
                            throw new Error(errData.error || `Error del servidor: ${response.status}`);
                        }).catch(() => {
                            throw new Error(`Error del servidor: ${response.status} - ${response.statusText}`);
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    datosClienteActual = data;
                    mostrarInfoCliente(data);
                })
                .catch(error => {
                    datosClienteActual = null; 
                    mostrarError(error.message);
                });
        });
    }

    function mostrarInfoCliente(data) {
        if (!infoClienteDiv) return;

        if(clienteTipoDocSpan) clienteTipoDocSpan.textContent = data.tipo_documento || 'N/A';
        if(clienteTipoDocAbrSpan) clienteTipoDocAbrSpan.textContent = data.tipo_documento_abreviatura || 'N/A';
        if(clienteNumDocSpan) clienteNumDocSpan.textContent = data.numero_documento || 'N/A';
        if(clienteNombreSpan) clienteNombreSpan.textContent = data.nombre || 'N/A';
        if(clienteApellidoSpan) clienteApellidoSpan.textContent = data.apellido || 'N/A';
        if(clienteCorreoSpan) clienteCorreoSpan.textContent = data.correo || 'N/A';
        if(clienteTelefonoSpan) clienteTelefonoSpan.textContent = data.telefono || 'N/A';
        
        infoClienteDiv.classList.remove('d-none');
        ocultarError();
    }

    function ocultarInfoCliente() {
        if (infoClienteDiv) {
            infoClienteDiv.classList.add('d-none');
        }
        datosClienteActual = null;
    }

    function mostrarError(mensaje) {
        if (!mensajeErrorDiv) return;
        mensajeErrorDiv.textContent = mensaje;
        mensajeErrorDiv.classList.remove('d-none');
        ocultarInfoCliente();
    }

    function ocultarError() {
        if (mensajeErrorDiv) {
            mensajeErrorDiv.classList.add('d-none');
        }
    }

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
        if (!data) return;

        let contenido = '';
        const nombreArchivoBase = `cliente_${data.numero_documento || 'desconocido'}`;
        let mimeType = '';
        let extension = formato;

        if (formato === 'csv') {
            contenido = "Campo,Valor\n";
            contenido += `Tipo Documento,"${data.tipo_documento || ''} (${data.tipo_documento_abreviatura || ''})"\n`;
            contenido += `Numero Documento,"${data.numero_documento || ''}"\n`;
            contenido += `Nombre,"${data.nombre || ''}"\n`;
            contenido += `Apellido,"${data.apellido || ''}"\n`;
            contenido += `Correo,"${data.correo || ''}"\n`;
            contenido += `Telefono,"${data.telefono || ''}"\n`;
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
            mimeType = 'text/plain';
        } else {
            return; // Formato no soportado
        }

        const blob = new Blob([contenido], { type: `${mimeType};charset=utf-8;` });
        const link = document.createElement("a");

        if (link.download !== undefined) {
            const url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", `${nombreArchivoBase}.${extension}`);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
        } else {
            alert("La descarga directa no es soportada por su navegador.");
        }
    }

    // Script para el cache-buster del enlace del reporte de fidelización
    const linkReporteFidelizacion = document.getElementById('linkReporteFidelizacion');
    if (linkReporteFidelizacion) {
        linkReporteFidelizacion.addEventListener('click', function(e) {
            e.preventDefault(); 
            const baseUrl = this.href;
            const timestamp = new Date().getTime();
            window.open(`${baseUrl}?t=${timestamp}`, '_blank'); 
        });
    }
});