from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ExampleSerializer, Example
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
