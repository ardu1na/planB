from django.contrib import admin
from unfold.admin import ModelAdmin

from alarms.models import *

class UsuariosInline(admin.StackedInline):
    model = Miembro

class CasaInline(admin.StackedInline):
    model = Casa    
    
class BarrioAdmin(ModelAdmin):
    inlines =  [CasaInline,]
admin.site.register(GrupoBarrial, BarrioAdmin)


class CasaAdmin(ModelAdmin):
    list_display = [ 'get_direccion_con_municipio_y_provincia', 'grupo_barrial', 'get_miembros_string']
    inlines =  [UsuariosInline,]
admin.site.register(Casa, CasaAdmin)


admin.site.register(Miembro)
admin.site.register(AlarmaEvent)