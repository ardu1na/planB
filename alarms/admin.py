from django.contrib import admin
from unfold.admin import ModelAdmin

from alarms.models import *

class UsuariosInline(admin.StackedInline):
    model = Miembro
    extra  = 0
    
    
class AlarmaInline(admin.StackedInline):
    model = AlarmaEvent    
    extra  = 0

class ViviendaInline(admin.StackedInline):
    model = Vivienda    
    extra  = 0

    
class BarrioAdmin(ModelAdmin):
    inlines =  [ViviendaInline,]

admin.site.register(AlarmaVecinal, BarrioAdmin)


class ViviendaAdmin(ModelAdmin):
    list_display = [ 'get_direccion_con_municipio_y_provincia', 'alarma_vecinal', 'get_miembros_string']
    inlines =  [UsuariosInline,]
admin.site.register(Vivienda, ViviendaAdmin)


class UsuarioAdmin(ModelAdmin):
    list_display = [ 'nombre', 'apellido', 'get_edad', 'get_barrio', 'vivienda']
    inlines =  [AlarmaInline,]
admin.site.register(Miembro, UsuarioAdmin)


admin.site.register(AlarmaEvent)