from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ExampleSerializer, Example
from .excel_upload_forms import UploadLibro1ExampleForm
from django.template import loader
from cotizadorFV.models_excel.inversor import Inversor
from django.http import HttpResponse, JsonResponse
import csv

def difference_between_csv_and_instance(dict_read, class_name):
	print('atributos en el csv y no en clase', set([x.lower() for x in dict_read.fieldnames]) - set(class_name().__dict__.keys() ))
	print('atributos en el clase y no en csv', set(class_name().__dict__.keys() )-set([x.lower() for x in dict_read.fieldnames]))

def lowercase_keys(d):
    result = {}
    for key, value in d.items():
        lower_case = key.lower()
        result[lower_case] = value
    return result
# Create your views here.
class ExampleView(APIView):
	def patch(self, request):
		exampleSerializer = ExampleSerializer(data=request.data)
		if (exampleSerializer.is_valid()):
			example = Example(a=exampleSerializer.data['a'], b=exampleSerializer.data['b'])
			print(example.a,example.b)
			return Response(exampleSerializer.data)
		else:
			return Response('nel')
	def get(self, request, format=None):
		"""
		Return a list of all users.
		"""
		example = Example('field_a', 'field_b')
		exampleSerializer = ExampleSerializer(example)
		example = Example(**exampleSerializer.data)
		print(example)
		return Response(exampleSerializer.data)


def upload_libro1_example(request):
	form = {}
	if request.method == 'POST':
		form = UploadLibro1ExampleForm(request.POST, request.FILES)
		print(request.FILES)
		libro1DictRead = csv.DictReader(request.FILES['file'],delimiter=';')
		difference_between_csv_and_instance(libro1DictRead, Inversor)
		try:
			print (Inversor(**lowercase_keys(libro1DictRead.next())).__dict__)
			return JsonResponse(Inversor(**lowercase_keys(libro1DictRead.next())).__dict__)
		except :
			return HttpResponse('nel')

	else:
		form = UploadLibro1ExampleForm()
	context = {
        'form': form,
    }
	template = loader.get_template('cotizadorFV/uploadlibro1example.html')
	return HttpResponse(template.render(context, request))