# -*- coding: utf-8 -*-
from rest_framework import status
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from .main_info import *
from cotizadorFV.modelsCSV import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from cotizadorFV.lib import lib as mainInfoLib
from django.http import HttpResponse            
from   lib.calculo_conductores import *  
from objetos_nativos_python_frontend import Generalfv
"""
# Create your views here.
"""
         


#Clases serializadoras para los archivos CSV
class InterruptorManualSerializerView(APIView):
    def get(self, request, format=None):
        serializer=[]
        interruptoresM=inicial.interruptoresManuales #se obtiene del arreglo inicial (que se carga al inicio cuanod se leen los excel) los interruptores manuales
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
        return Response(serializer)
        
class DpsDCView(APIView):
    def get(self, request, format=None):
        serializer=[]
        for interruptor in inicial.dpssDC:
            serializer.append(DpsDCSerializer(interruptor).data)
        return Response(serializer)
        
class Inversoriew(APIView):
    def get(self, request, format=None):
        serializer=[]
        inversores=inicial.inversores
        for interruptor in inversores:
            serializer.append(InversorSerializer(interruptor).data)
        return Response(serializer) 


class MicroInversoriew(APIView):
    def get(self, request, format=None):
        serializer=[]
        microInversores=inicial.microInversores
        for interruptor in microInversores:
            serializer.append(MicroInversorSerializer(interruptor).data)
        return Response(serializer)      
        

class PanelSolarView(APIView):
    def get(self, request, format=None):
        serializer=[]
        PanelSolar=inicial.panelesSolares
        for interruptor in PanelSolar:
            serializer.append(PanelSolarSerializer(interruptor).data)
        return Response(serializer) 
        
class FusibleView(APIView):
    def get(self, request, format=None):
        serializer=[]
        for interruptor in inicial.fusibles:
            serializer.append(FusibleSerializer(interruptor).data)
        return Response(serializer) 
      

class InteAutoView(APIView):
    def get(self, request, format=None):
        serializer=[]
        for interruptor in inicial.interruptoresAutomaticos:
            serializer.append(InteAutoSerializer(interruptor).data)
        return Response(serializer) 
        
# Realiza la  serialización de los archivos CSV, ante peticion get__________
        
class DataCsvView(APIView):
    def get(self, request, format=None):
        serializer = DataSerializer(mainInfoLib.getData())
        return Response(serializer.data)
        
        
    
    
    
#___________________________________________________________________-

class deserializacion (APIView):
    
    def post(self, request, format=None):
        serializer = GeneralFVSerializer(data=request.data)
        if serializer.is_valid():
            print  serializer.validated_data
            generalFv=getGeneralFvNativeObject(serializer.data)
            lectura(generalFv)
            
            return  HttpResponseRedirect(redirect_to='https://simulador-fv-paolamedina.c9users.io/cotizadorFV/cotizacion/')

        else:
            return Response(serializer.errors,  status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            


       
def getGeneralFvNativeObject(serializer):
    generalfv=Generalfv(serializer['potencia_de_planta_fv'],serializer['nombre_proyecto'],serializer['temperatura_ambiente'],
    serializer['minima_temperatura_ambiente_esperada'],serializer['tipo_de_inversor'],
    serializer['lugar_instalacion_opcion_techo_cubierta'],serializer['tipo_servicio'],serializer['voltage_servicio'],
    serializer['lugar_instalacion'],serializer['fvs'])
    mttps= generalfv.fvs[0].mttps
    return generalfv
            
  
def lectura(generalFv):
    dic_main=mainInfoLib.getDic() #diccionario principal con los datos cargados de excel
    conductoresMttp=[]#matriz de los calibres de entrada y salida de los mppts
    conductoresInversor=[] #matriz de los calibres de entrada y salida de los inversores de campos fv
    conductoresAC=[]#matriz de los calibres de entrada y salida de los inversores de campos fv para coductores AC
    tem_amb=generalFv.temperatura_ambiente
    tensionServicio=float(generalFv.voltage_servicio)
    #print tensionServicio
   
    #print "tem_amb "+ str(tem_amb)
    for panelfv in  generalFv.fvs:
        isc_panel=float(dic_main.panelesSolares_dict[panelfv.model_panel_solar_1].isc)
        #print "isc_panel "+ str(isc_panel)
        vmmp_panel=float(dic_main.panelesSolares_dict[panelfv.model_panel_solar_1].vmpp)
        #print "vmmp_panel "+ str(vmmp_panel)
        impp_panel=float(dic_main.panelesSolares_dict[panelfv.model_panel_solar_1].impp)
        #print "impp_panel "+ str(impp_panel)
        max_conductInInversor=panelfv.salida_inversor.input.maximo_numero_de_conductores
        max_conductOutInversor=panelfv.salida_inversor.output.maximo_numero_de_conductores
        distanciaConductOutInversor=panelfv.salida_inversor.output.distancia_del_conductor_mas_largo
        #print distanciaConductOutInversor
        caidaTensionUsuarioSalida=panelfv.salida_inversor.output.caida_de_tension_de_diseno
        #print caidaTensionUsuarioSalida
        
        #calculo de conductores para salida inversor
        inversor=panelfv.modelo_panel_solar_2#modelo del inversor
        isalFuente=isalN(inversor,tensionServicio)
        isalSalida=sumIsal(inversor)
        conductorInversor=CalculoConductoresInversor(isalFuente,isalSalida,tem_amb,max_conductInInversor,max_conductOutInversor,isc_panel,
                                                        distanciaConductOutInversor,tensionServicio,caidaTensionUsuarioSalida)
        conductoresInversor.append(conductorInversor)
        
        #calculo de conductores puesto a tierra DC
        conductorDC=calibreconductorDC(panelfv.mttps,isc_panel)
        
        #calculo de conductores puesto a tierra AC
        conductorAC=calibreconductorAC(isalFuente,isalSalida,tem_amb,max_conductInInversor,max_conductOutInversor,isc_panel)
        conductoresAC.append(conductorAC)
        
        for mppt in panelfv.mttps:
            cadenas_paralelo= mppt.numero_de_cadenas_en_paralelo
            #print "cadenas_paralelo " + str(cadenas_paralelo)
            max_conductoresFuente= mppt.cableado.input.maximo_numero_de_conductores
            #print "max_conductoresFuente " + str(max_conductoresFuente)
            max_conductoresSalida=mppt.cableado.output.maximo_numero_de_conductores
            #print "max_conductoresSalida " + str(max_conductoresSalida)
            distanciaConductorFuente= mppt.cableado.input.distancia_del_conductor_mas_largo
            #print "distanciaConductorFuente " + str(distanciaConductorFuente)
            distanciaConductorSalida= mppt.cableado.output.distancia_del_conductor_mas_largo
            #print "distanciaConductorSalida " + str(distanciaConductorSalida)
            corrienteMPP= cadenas_paralelo * impp_panel
            #print "corrienteMPP " + str(corrienteMPP)
            tension_Mpp= mppt.numero_de_paneles_en_serie_por_cadena  * vmmp_panel
            #print "tension_Mpp " + str(tension_Mpp)
            tensionFuenteDiseno= mppt.cableado.input.caida_de_tension_de_diseno
            #print "tensionFuenteDiseno " + str(tensionFuenteDiseno)
            tensionSalidaDiseno= mppt.cableado.output.caida_de_tension_de_diseno
            #print "tensionSalidaDiseno " + str(tensionSalidaDiseno)
            tipo_alambradoEntrada=mppt.cableado.input.tipo_alambrado
            #print "tipo_alambradoEntrada "+ tipo_alambradoEntrada
            tipo_alambradoSalida=mppt.cableado.output.tipo_alambrado
            #print "tipo_alambradoSalida "+ tipo_alambradoSalida
            
            condutor=CalculoConductores(tem_amb,max_conductoresFuente,max_conductoresSalida,isc_panel,impp_panel,
                            cadenas_paralelo,distanciaConductorFuente,distanciaConductorSalida,corrienteMPP,tension_Mpp,
                            tensionFuenteDiseno,tensionSalidaDiseno,tipo_alambradoEntrada,tipo_alambradoSalida)
            conductoresMttp.append(condutor)    
            
            
 
    
    #print dic_main.panelesSolares_dict[panel].isc
    #print "temperatura "+ str(tem_amb)
    print "conductores mppt"
    print conductoresMttp
    print "conductores inversor"
    print conductoresInversor
    print "conductorDC " + str(conductorDC)
    print "conductorAC "
    print conductoresAC
    

#funcion que determina el Isal_max de la base de datos inversores dependiendo inversor y el Vsal seleccionado en la cotización  
def isalN(inversor,tensionServicio):
    dic_main=mainInfoLib.getDic() #diccionario principal con los datos cargados de excel
    isal=0
    isal_max_1=float(dic_main.inversores_dict[inversor].isal_max_1)
    isal_max_2=float(dic_main.inversores_dict[inversor].isal_max_2)
    isal_max_3=float(dic_main.inversores_dict[inversor].isal_max_3)
    if (tensionServicio==dic_main.inversores_dict[inversor].vsal_1):
        isal=isal_max_1
    elif(tensionServicio==dic_main.inversores_dict[inversor].vsal_2):
        isal=isal_max_2
    elif (tensionServicio==dic_main.inversores_dict[inversor].vsal_3):
        isal=isal_max_3
        
    return isal
 
#funcion que suma todos los Isal_max de la base de datos del inversor segun el inversor seleccionado  
def sumIsal(inversor):
    dic_main=mainInfoLib.getDic() #diccionario principal con los datos cargados de excel
    isal_max_1=float(dic_main.inversores_dict[inversor].isal_max_1)
    isal_max_2=float(dic_main.inversores_dict[inversor].isal_max_2)
    isal_max_3=float(dic_main.inversores_dict[inversor].isal_max_3)
    return isal_max_1+isal_max_1+isal_max_1
    
def cotizador(request):
    return render(request, 'formulario.html')
    
    
    
def calculos(request):
    seleccionCalibre(30,10,4,9.82,8.28,4,500,200,33.12,92.4,20,20,'','')
    return HttpResponse("hola")