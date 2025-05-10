from django.urls import path
from . import views

app_name = 'sac_app'

urlpatterns = [
    path('', views.pagina_consulta_cliente, name='pagina_consulta_cliente'),
    path('api/cliente/consulta/<str:numero_documento>/', views.consultar_cliente_api, name='consultar_cliente_api'),
    path('reportes/fidelizacion/excel/', views.generar_reporte_fidelizacion_excel, name='reporte_fidelizacion_excel'),
]