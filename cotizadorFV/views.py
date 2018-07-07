from django.shortcuts import render
from .models_excel import *
from main_info import *
from cotizadorFV.modelsCVS import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import InteManualSerializer

"""
# Create your views here.
"""
         

class InterruptorManualSerializerView(APIView):
    def get(self, request, format=None):
        serializer=[]
        interruptoresM=inicial.interruptores_manuales
        for interruptor in interruptoresM:
            serializer.append(InteManualSerializer(interruptor).data)
            #example = InterruptorManual(**exampleSerializer.data)
            #print(example.descripcion)
        return Response(serializer)
