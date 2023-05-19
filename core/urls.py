
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from dashboard.dashboard_views import get_sos, get_emergencia, get_fuego, success

urlpatterns = [
    
    
    ## envios de alertas desde el dispositivo del usuario a través de google home y estos links:
    path('s/<uuid:pk>/', get_sos, name="sos"), 
    path('e/<uuid:pk>/', get_emergencia, name="emergencia"), 
    path('f/<uuid:pk>/', get_fuego, name="fuego"),  
    
    path('alerta-enviada/<uuid:pk>/', success, name="success"),  

    path('',  include('dashboard.urls', namespace='dashboard')),   




    path('admin/', admin.site.urls),
   
    #Dashboard
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),

    #Frontend
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

