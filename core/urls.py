"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from dashboard.dashboard_views import get_sos, get_emergencia, get_fuego

urlpatterns = [
    
    
    ## envios de alertas desde el dispositivo del usuario a través de google home y estos links:
    path('s/<uuid:pk>/', get_sos, name="sos"), 
    path('e/<uuid:pk>/', get_emergencia, name="emergencia"), 
    path('f/<uuid:pk>/', get_fuego, name="fuego"),  
    
    path('admin/', admin.site.urls),
   
    #Dashboard
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),

    #Frontend
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

