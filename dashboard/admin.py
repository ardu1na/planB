from django.contrib import admin
from dashboard.models import Configurations
from unfold.admin import ModelAdmin

class ConfAdmin(ModelAdmin):
    pass
admin.site.register(Configurations, ConfAdmin)

# Register your models here.
