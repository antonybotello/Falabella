from django.http import JsonResponse, HttpResponse
from django.shortcuts import render 
from .models import Cliente, Compra
from django.utils import timezone
from datetime import datetime, timedelta
import pandas as pd
import io

def pagina_consulta_cliente(request):
    """
    Renderiza la plantilla principal 'index.html' para la consulta de clientes.
    Opcionalmente, podría cargar y pasar al contexto los tipos de documento
    si se decidiera poblarlos dinámicamente en el <select> del formulario.
    """
    # Ejemplo de cómo pasar los tipos de documento al contexto (opcional):
    # tipos_documento = TipoDocumento.objects.all().order_by('nombre_tipo')
    # context = {
    #     'tipos_documento_opciones': tipos_documento 
    # }
    # return render(request, 'sac_app/index.html', context)
    
    # Versión simple que solo renderiza la plantilla:
    return render(request, 'sac_app/index.html')

def consultar_cliente_api(request, numero_documento):
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
               
            }
            return JsonResponse(datos_cliente, status=200)

        except Cliente.DoesNotExist:
            return JsonResponse({'error': 'Cliente no encontrado'}, status=404)
        except Exception as e:
        
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
# sac_app/views.py
from django.shortcuts import render # Asegúrate que render esté importado

# ... (otras importaciones) ...

def generar_reporte_fidelizacion_excel(request):
    if request.method == 'GET':
        try:
            # ... (lógica para calcular fechas_inicio_reporte y fecha_fin_reporte) ...
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
                    'mensaje': "No hay compras registradas en el último mes para generar el reporte. Por favor, verifique los datos de compra.",
                    'tipo_mensaje': "warning" # o 'info'
                }
                return render(request, 'sac_app/reporte_mensaje.html', context, status=404)

            # ... (lógica de Pandas) ...
            data_compras = [] # ... (poblar data_compras) ...
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

            if df_compras.empty: # Aunque el QuerySet ya lo verificó, es una doble comprobación
                context = {
                    'mensaje': "No hay datos de compras procesables para el último mes después de la conversión.",
                    'tipo_mensaje': "warning"
                }
                return render(request, 'sac_app/reporte_mensaje.html', context, status=404)

            # ... (resto de la lógica de Pandas para agrupar y filtrar) ...
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
                return render(request, 'sac_app/reporte_mensaje.html', context, status=404) # O status 200 si consideras que es una respuesta válida sin datos

            # ... (lógica para generar y devolver el Excel) ...
            # Si todo va bien y se genera el Excel:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_clientes_fidelizar_final.to_excel(writer, sheet_name='Clientes Fidelizados', index=False)
            output.seek(0)

            nombre_archivo = f"reporte_fidelizacion_{fecha_inicio_reporte.strftime('%Y-%m')}.xlsx"
            response = HttpResponse(
                output,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
            return response

        except Exception as e:
            # Loggear el error 'e'
            context = {
                'mensaje': f"Error interno generando el reporte: {e}",
                'tipo_mensaje': "error"
            }
            return render(request, 'sac_app/reporte_mensaje.html', context, status=500)
    else:
        context = {
            'mensaje': "Método no permitido para esta solicitud.",
            'tipo_mensaje': "error"
        }
        return render(request, 'sac_app/reporte_mensaje.html', context, status=405)