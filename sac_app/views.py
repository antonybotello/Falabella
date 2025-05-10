from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
import pandas as pd
import io

# Importar tus modelos
from .models import Cliente, Compra, TipoDocumento 


def pagina_consulta_cliente(request):
    """
    Renderiza la plantilla principal 'index.html' para la consulta de clientes.
    """
    return render(request, 'sac_app/index.html')


def consultar_cliente_api(request, numero_documento):
    """
    API para consultar la información de un cliente por su número de documento.
    Devuelve datos del cliente en formato JSON.
    """
    if request.method == 'GET':
        try:
            cliente = Cliente.objects.select_related('tipo_documento').get(numero_documento=numero_documento)
            
            datos_cliente = {
                'numero_documento': cliente.numero_documento,
                'tipo_documento': cliente.tipo_documento.nombre_tipo,
                'tipo_documento_abreviatura': cliente.tipo_documento.abreviatura,
                'nombre': cliente.nombre,
                'apellido': cliente.apellido,
                'correo': cliente.correo,
                'telefono': cliente.telefono,
                # Puedes añadir más campos aquí si son necesarios para el frontend
            }
            return JsonResponse(datos_cliente, status=200)
        
        except Cliente.DoesNotExist:
            return JsonResponse({'error': 'Cliente no encontrado'}, status=404)
        except Exception as e:
            # En un entorno de producción, se registraría este error 'e'
            # print(f"Error en consultar_cliente_api: {e}") # Para depuración en desarrollo si es necesario
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


def generar_reporte_fidelizacion_excel(request):
    """
    Genera un reporte en Excel de los clientes fidelizados basado en sus compras
    del último mes y lo devuelve como una descarga de archivo.
    """
    if request.method == 'GET':
        try:
            hoy = timezone.now()
            primer_dia_mes_actual = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            ultimo_dia_mes_pasado = primer_dia_mes_actual - timedelta(days=1)
            primer_dia_mes_pasado = ultimo_dia_mes_pasado.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            fecha_inicio_reporte = primer_dia_mes_pasado
            fecha_fin_reporte = ultimo_dia_mes_pasado.replace(hour=23, minute=59, second=59, microsecond=999999)

            compras_ultimo_mes = Compra.objects.filter(
                fecha_compra__gte=fecha_inicio_reporte,
                fecha_compra__lte=fecha_fin_reporte
            ).select_related('cliente', 'cliente__tipo_documento')

            if not compras_ultimo_mes.exists():
                context = {
                    'mensaje': f"No hay compras registradas en el último mes ({fecha_inicio_reporte.strftime('%B %Y')}) para generar el reporte. Por favor, verifique los datos de compra.",
                    'tipo_mensaje': "warning"
                }
                return render(request, 'sac_app/reporte_mensaje.html', context, status=404)

            data_compras = []
            for compra in compras_ultimo_mes:
                data_compras.append({
                    'cliente_id': compra.cliente.id,
                    'numero_documento': compra.cliente.numero_documento,
                    'tipo_documento': compra.cliente.tipo_documento.abreviatura,
                    'nombre_cliente': f"{compra.cliente.nombre} {compra.cliente.apellido}",
                    'correo_cliente': compra.cliente.correo,
                    'telefono_cliente': compra.cliente.telefono,
                    'monto_compra': float(compra.monto_compra)
                })
            
            df_compras = pd.DataFrame(data_compras)

            if df_compras.empty: # Aunque .exists() ya lo cubrió, es una doble verificación
                context = {
                    'mensaje': "No hay datos de compras procesables para el último mes después de la conversión.",
                    'tipo_mensaje': "warning"
                }
                return render(request, 'sac_app/reporte_mensaje.html', context, status=404)

            df_clientes_fidelizar = df_compras.groupby(
                ['cliente_id', 'numero_documento', 'tipo_documento', 'nombre_cliente', 'correo_cliente', 'telefono_cliente']
            )['monto_compra'].sum().reset_index()
            
            df_clientes_fidelizar.rename(columns={'monto_compra': 'monto_total_compras_ultimo_mes'}, inplace=True)

            monto_minimo_fidelizacion = 5000000
            df_clientes_fidelizar_final = df_clientes_fidelizar[df_clientes_fidelizar['monto_total_compras_ultimo_mes'] > monto_minimo_fidelizacion]

            if df_clientes_fidelizar_final.empty:
                context = {
                    'mensaje': f"Ningún cliente supera el monto de compras de ${monto_minimo_fidelizacion:,.0f} COP en el último mes ({fecha_inicio_reporte.strftime('%B %Y')}).",
                    'tipo_mensaje': "info"
                }
                return render(request, 'sac_app/reporte_mensaje.html', context, status=200) 

            output = io.BytesIO()
            try:
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_clientes_fidelizar_final.to_excel(writer, sheet_name='Clientes Fidelizados', index=False)
                excel_bytes = output.getvalue()
            finally:
                if output: # Asegurarse de que el buffer se cierre
                    output.close()

            nombre_archivo = f"reporte_fidelizacion_{fecha_inicio_reporte.strftime('%Y-%m')}.xlsx"
            
            response = HttpResponse(
                excel_bytes,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
            
            # Cabeceras Anti-Caché
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0' 
            return response

        except Exception as e:
            context = {
                'mensaje': f"Se produjo un error interno generando el reporte. Por favor, contacte al administrador. (Detalle: {str(e)})",
                'tipo_mensaje': "error"
            }
            return render(request, 'sac_app/reporte_mensaje.html', context, status=500)
    else:
        context = {
            'mensaje': "Método no permitido para esta solicitud. Solo se acepta GET.",
            'tipo_mensaje': "error"
        }
        return render(request, 'sac_app/reporte_mensaje.html', context, status=405)