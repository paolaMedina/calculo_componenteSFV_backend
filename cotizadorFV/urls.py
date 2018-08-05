from django.conf.urls import url
from . import views
from .views import  cotizador
urlpatterns = [
    url(r'^interruptoresManuales/$', views.InterruptorManualSerializerView.as_view(), name='interruptoresManuales'),
    url(r'^DpsACView/$', views.DpsACView.as_view(), name='DpsACView'),
    url(r'^MicroInversoriew/$', views.MicroInversoriew.as_view(), name='MicroInversoriew'),
    url(r'^PanelSolarView/$', views.PanelSolarView.as_view(), name='PanelSolarView'),
    url(r'^Inversoriew/$', views.Inversoriew.as_view(), name='Inversoriew'),
    url(r'^DpsDCView/$', views.DpsDCView.as_view(), name='DpsDCView'),
    url(r'^FusibleView/$', views.FusibleView.as_view(), name='FusibleView'),
    url(r'^InteAutoView/$', views.InteAutoView.as_view(), name='InteAutoView'),
    
    url(r'^csvData/$', views.DataCsvView.as_view(), name='csvData'),
    
    url(r'^postData/$', views.deserializacion.as_view(), name='postData'),
    
    url(r'^l/$', views.calculos, name='l'),
    
    url (r'^cotizacion/$', cotizador, name='cotizacion' )
    
]