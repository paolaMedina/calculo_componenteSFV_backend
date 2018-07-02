from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ExampleSerializer, Example
# Create your views here.
"""
calculate():
    deserialize(cotization ):
        pdf = lib.generatepdf(cotization)"""
class ExampleView(APIView):
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        example = Example('field_a', 'field_b')
        exampleSerializer = ExampleSerializer(example)
        example = Example(**exampleSerializer.data)
        print(example.a)
        return Response(exampleSerializer.data)