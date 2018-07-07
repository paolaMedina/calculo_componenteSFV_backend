from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^interruptoresManuales/$', views.InterruptorManualSerializerView.as_view(), name='interruptoresManuales'),
     url(r'^csvData/$', views.DataCsvView.as_view(), name='csvData'),
]