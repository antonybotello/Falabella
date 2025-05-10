from django.contrib import admin
from .models import TipoDocumento, Cliente, Compra

@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre_tipo', 'abreviatura')
    search_fields = ('nombre_tipo', 'abreviatura')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('numero_documento', 'nombre', 'apellido', 'tipo_documento', 'correo', 'telefono', 'fecha_registro')
    list_filter = ('tipo_documento', 'fecha_registro')
    search_fields = ('nombre', 'apellido', 'numero_documento', 'correo')
    raw_id_fields = ('tipo_documento',) 

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha_compra', 'monto_compra')
    list_filter = ('fecha_compra', 'cliente__tipo_documento') 
    search_fields = ('cliente__nombre', 'cliente__apellido', 'cliente__numero_documento')
    autocomplete_fields = ['cliente'] 
    date_hierarchy = 'fecha_compra'