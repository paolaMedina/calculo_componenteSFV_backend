from django.shortcuts import render
from .models_excel import *
from .main_info import *
from cotizadorFV.modelsCSV import *
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
        interruptoresM=inicial.interruptoresManuales
        for interruptor in interruptoresM:
            serializer.append(InteManualSerializer(interruptor).data)
            #example = InterruptorManual(**exampleSerializer.data)
        return Response(serializer)
        

class DpsACView(APIView):
    def get(self, request, format=None):
        serializer=[]
        DpsAC=inicial.dpssAC
        for interruptor in DpsAC:
            serializer.append(DpsACSerializer(interruptor).data)
            #example = InterruptorManual(**exampleSerializer.data)
        return Response(serializer)
        
class DpsDCView(APIView):
    def get(self, request, format=None):
        serializer=[]
        for interruptor in inicial.dpssDC:
            serializer.append(DpsDCSerializer(interruptor).data)
            #example = InterruptorManual(**exampleSerializer.data)
        return Response(serializer)
        
class Inversoriew(APIView):
    def get(self, request, format=None):
        serializer=[]
        inversores=inicial.inversores
        for interruptor in inversores:
            serializer.append(InversorSerializer(interruptor).data)
            #example = InterruptorManual(**exampleSerializer.data)
        return Response(serializer) 


class MicroInversoriew(APIView):
    def get(self, request, format=None):
        serializer=[]
        microInversores=inicial.microInversores
        for interruptor in microInversores:
            serializer.append(MicroInversorSerializer(interruptor).data)
            #example = InterruptorManual(**exampleSerializer.data)
        return Response(serializer)      
        

class PanelSolarView(APIView):
    def get(self, request, format=None):
        serializer=[]
        PanelSolar=inicial.panelesSolares
        for interruptor in PanelSolar:
            serializer.append(PanelSolarSerializer(interruptor).data)
            #example = InterruptorManual(**exampleSerializer.data)
        return Response(serializer) 
        
class FusibleView(APIView):
    def get(self, request, format=None):
        serializer=[]
        for interruptor in inicial.fusibles:
            serializer.append(FusibleSerializer(interruptor).data)
            #example = InterruptorManual(**exampleSerializer.data)
        return Response(serializer) 
      

class InteAutoView(APIView):
    def get(self, request, format=None):
        serializer=[]
        for interruptor in inicial.interruptoresAutomaticos:
            serializer.append(InteAutoSerializer(interruptor).data)
            #example = InterruptorManual(**exampleSerializer.data)
        return Response(serializer) 
        
#______________________________________________________
        
class DataCsvView(APIView):
    def get(self, request, format=None):
        serializer = DataSerializer(mainInfoLib.getData())
        return Response(serializer.data)