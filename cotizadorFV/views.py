from django.shortcuts import render
from .models_excel import *
from main_info import *
from cotizadorFV.modelsCVS import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from cotizadorFV.models_excel import lib as mainInfoLib

"""
# Create your views here.
"""
         

class InterruptorManualSerializerView(APIView):
    def get(self, request, format=None):
        serializer=[]
        interruptoresM=inicial.dpssAC
        for interruptor in interruptoresM:
            serializer.append(DpsACSerializer(interruptor).data)
            #example = InterruptorManual(**exampleSerializer.data)
        return Response(serializer)
        
        
class DataCsvView(APIView):
    def get(self, request, format=None):
        serializer = DataSerializer(mainInfoLib.getData())
        return Response(serializer.data)