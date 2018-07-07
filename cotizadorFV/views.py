from django.shortcuts import render
from .models_excel import *
from main_info import *
from cotizadorFV.modelsCVS import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ExampleSerializer, Example, InteManualSerializer

"""
# Create your views here.
"""

def importcsv(modelo, archivo):
    
    if (modelo=='InterruptorManual'):
        my_csv_list = InterruptorManual.import_data(data = open(archivo))
        
        for i in range(1, len(my_csv_list)):
            line = my_csv_list[i]
            inicial.interruptores_manuales.append(line)
    else :
        0
    
    for a in inicial.interruptores_manuales:
          print a.descripcion
         

class InterruptorManualSerializerView(APIView):
    def get(self, request, format=None):
        serializer=[]
        interruptoresM=inicial.interruptores_manuales
        for interruptor in interruptoresM:
            serializer.append(InteManualSerializer(interruptor).data)
            #example = InterruptorManual(**exampleSerializer.data)
            #print(example.descripcion)
        return Response(serializer)
