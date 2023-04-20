from django.contrib import admin
from unfold.admin import ModelAdmin

from alarms.models import *

class UsuariosInline(admin.StackedInline):
    model = Miembro

class ViviendaInline(admin.StackedInline):
    model = Vivienda    
    
class BarrioAdmin(ModelAdmin):
    inlines =  [ViviendaInline,]
admin.site.register(AlarmaVecinal, BarrioAdmin)


class ViviendaAdmin(ModelAdmin):
    list_display = [ 'get_direccion_con_municipio_y_provincia', 'alarma_vecinal', 'get_miembros_string']
    inlines =  [UsuariosInline,]
admin.site.register(Vivienda, ViviendaAdmin)


admin.site.register(Miembro)
admin.site.register(AlarmaEvent)