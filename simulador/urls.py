"""simulador URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.conf.urls import handler404,handler500
from django.contrib import admin

from cotizadorFV.models import *
from cotizadorFV.views import *
from .views import Home,loginPage
from cotizadorFV.lib.lib import importarCsvs
from django.contrib.auth.views import logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete


importarCsvs() #carga inicial de los archivos csv


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login', loginPage, name='loginPage'), 
    url(r'^Home', Home, name='inicio'), 
    url(r'^cotizadorFV/', include('cotizadorFV.urls', namespace="cotizadorFv")),
    url(r'^fileupload/', include('cargaArchivos.urls', namespace="cargarArchivos")),
    url(r'^usuario/', include('usuario.urls', namespace="usuario")),
    
    
    
    url(r'^reset/password_reset/$',password_reset,{'template_name':'password_reset.html',
    'email_template_name':'password_reset_email.html'},name="password_reset"),
    url(r'^password_reset_done/$', password_reset_done, {'template_name':'password_reset_done.html'},name="password_reset_done"),
   
    url(r'^reset/(?P<uidb64>[0-94-Za-z_\-]+)/(?P<token>.+)/$',password_reset_confirm,{'template_name':'password_reset_confirm.html'},name="password_reset_confirm"), 
    url(r'^reset/done',password_reset_complete,{'template_name':'password_reset_complete.html'},name="password_reset_complete"),
 
]
#handler404 = 'simulador.views.handler404'
#handler500 = 'simulador.views.handler500'

#para descargar archivos
from django.conf.urls.static import  static
from django.conf import settings
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)