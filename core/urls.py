
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from dashboard.dashboard_views import sos, emergencia, fuego, success

urlpatterns = [
    
    
    ## envios de alertas desde el dispositivo del usuario a través de google home y estos links:
    path('s/', sos, name="sos"), 
    path('e/', emergencia, name="emergencia"), 
    path('f/', fuego, name="fuego"),  
    
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

