from django.conf.urls import url
from . import views

urlpatterns = [
    url('exampleserializers', views.ExampleView.as_view(), name='index'),
    url('uploadlibro1example', views.upload_libro1_example, name='uploadlibroexample'),
]