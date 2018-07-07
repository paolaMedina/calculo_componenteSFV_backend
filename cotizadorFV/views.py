from django.shortcuts import render
from .models_excel import *
from main_info import *
from cotizadorFV.modelsCVS import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import InteManualSerializer, DataSerializer

"""
# Create your views here.
"""
         

class InterruptorManualSerializerView(APIView):
    def get(self, request, format=None):
        serializer=[]
        interruptoresM=inicial.interruptoresManuales
        for interruptor in interruptoresM:
            serializer.append(InteManualSerializer(interruptor).data)
            #example = InterruptorManual(**exampleSerializer.data)
        return Response(serializer)
class DataCsvView(APIView):
    def get(self, request, format=None):
        serializer = DataSerializer(inicial)
        return Response(serializer.data)