from django.conf.urls import url
from . import views
from .views import  cotizador,viewSendPDF,alonePdf
urlpatterns = [
    url(r'^csvData/$', views.DataCsvView.as_view(), name='csvData'),
    url(r'^postData/$', views.deserializacion.as_view(), name='postData'),
    url(r'^postData2/$', views.deserializacion2.as_view(), name='postData2'),
    url (r'^cotizacion/$', cotizador, name='cotizacion' ),
    url ('pdf/(?P<filename>[\w-]+)/$', viewSendPDF,name='pdf'),
    url (r'pdf/$', alonePdf,name='viewpdf'),
    ]
"""url(r'^interruptoresManuales/$', views.InterruptorManualSerializerView.as_view(), name='interruptoresManuales'),
url(r'^DpsACView/$', views.DpsACView.as_view(), name='DpsACView'),
url(r'^MicroInversoriew/$', views.MicroInversoriew.as_view(), name='MicroInversoriew'),
url(r'^PanelSolarView/$', views.PanelSolarView.as_view(), name='PanelSolarView'),
url(r'^Inversoriew/$', views.Inversoriew.as_view(), name='Inversoriew'),
url(r'^DpsDCView/$', views.DpsDCView.as_view(), name='DpsDCView'),
url(r'^FusibleView/$', views.FusibleView.as_view(), name='FusibleView'),
url(r'^InteAutoView/$', views.InteAutoView.as_view(), name='InteAutoView'),"""
