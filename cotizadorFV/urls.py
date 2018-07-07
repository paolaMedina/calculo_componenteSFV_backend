from django.conf.urls import url
from . import views

urlpatterns = [
    url('', views.InterruptorManualSerializerView.as_view(), name='index'),
]