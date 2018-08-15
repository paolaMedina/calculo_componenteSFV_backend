# -*- coding: utf-8 -*-
from rest_framework import status
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from rest_framework.permissions import AllowAny
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
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        serializer = GeneralFVSerializer(data=request.data)
        if serializer.is_valid():
            print "valido"
            #print  serializer.validated_data
            generalFv=getGeneralFvNativeObject(serializer.data)
            lectura(generalFv)
            messages.success(self.request, "Cotizacion")
            return  HttpResponseRedirect(redirect_to='https://simulador-fv-paolamedina.c9users.io/cotizadorFV/cotizacion/')

        else:
            print "invalido"
            print serializer.errors
            return Response(serializer.errors,  status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            


       
def getGeneralFvNativeObject(serializer):
    generalfv=Generalfv(serializer['potencia_de_planta_fv'],serializer['nombre_proyecto'],serializer['temperatura_ambiente'],
    serializer['minima_temperatura_ambiente_esperada'],serializer['tipo_de_inversor'],
    serializer['lugar_instalacion_opcion_techo_cubierta'],serializer['tipo_servicio'],serializer['voltage_servicio'],
    serializer['lugar_instalacion'],serializer['combinacion_inversor'],serializer['fvs'])
    mttps= generalfv.fvs[0].mttps
    #print "combi "+ generalfv.combinacion_inversor
    return generalfv
            
  
def lectura(generalFv):
    dic_main=mainInfoLib.getDic() #diccionario principal con los datos cargados de excel
    conductoresMttp=[]#matriz de los calibres de entrada y salida de los mppts
    conductoresInversor=[] #matriz de los calibres de entrada y salida de los inversores de campos fv
    itemsDpsDC=[]
    itemInterruptorDC=[]
    itemsDpsACSalida=[]
    fusibles=[]
    interruptoresAutoSalidaInversor=[]
    sumCorriente_Int=0
    sumaIsal=0
    
    cajasCombinadorasMppt=[]#arreglo de la caja combinadora que sale por cada mppt de cada panel
    cajasCombinadorasFinal=[]#las cajas por cada panel 
    
    tem_amb=generalFv.temperatura_ambiente
    temp_ambiente_mas_baja_esperada=generalFv.minima_temperatura_ambiente_esperada
    tensionServicio=float(generalFv.voltage_servicio)
    tipoServicio=generalFv.tipo_servicio
    lugar_instalacion=generalFv.lugar_instalacion
    lugar_instalacion_opcion_techo_cubierta=generalFv.lugar_instalacion_opcion_techo_cubierta
    max_conductCombinacionInversor=generalFv.combinacion_inversor.input.maximo_numero_de_conductores
    distanciaCombinacionInversor=generalFv.combinacion_inversor.input.distancia_del_conductor_mas_largo
    caidaTensionCombinacionInversor=generalFv.combinacion_inversor.input.caida_de_tension_de_diseno
    
    itemDpsACInyeccion=calculoDpsACInyeccion(lugar_instalacion, lugar_instalacion_opcion_techo_cubierta, tipoServicio,tensionServicio)
    paneles_agrupados=calculoPanelesSolares(generalFv.fvs)
    for panelfv in  generalFv.fvs:
        isc_panel=float(dic_main.panelesSolares_dict[panelfv.model_panel_solar_1].isc)
        vmmp_panel=float(dic_main.panelesSolares_dict[panelfv.model_panel_solar_1].vmpp)
        impp_panel=float(dic_main.panelesSolares_dict[panelfv.model_panel_solar_1].impp)
        voc_panel=float(dic_main.panelesSolares_dict[panelfv.model_panel_solar_1].voc)
        coef_voc_panel=float(dic_main.panelesSolares_dict[panelfv.model_panel_solar_1].coef_voc.replace("%","").replace(',','.'))
    
        
        max_conductOutInversor=panelfv.salida_inversor.output.maximo_numero_de_conductores
        distanciaConductOutInversor=panelfv.salida_inversor.output.distancia_del_conductor_mas_largo
        caidaTensionUsuarioSalida=panelfv.salida_inversor.output.caida_de_tension_de_diseno
        
        #calculo de conductores para salida inversor
        inversor=panelfv.modelo_panel_solar_2#modelo del inversor
        isalInversor=isalN(inversor,tensionServicio)
        sumaIsal+=isalInversor#acumulado de los isal de cada salida inversor
        conductorInversor=CalculoConductorInversor(tipoServicio,isalInversor,tem_amb,max_conductOutInversor,isc_panel,
                                                        distanciaConductOutInversor,tensionServicio,caidaTensionUsuarioSalida)
        conductoresInversor.append(conductorInversor)
        
        #calculo de conductores puesto a tierra DC
        conductorDC=calibreconductorDC(panelfv.mttps,isc_panel)
        
        #Calculo DPS AC (Salida inversores)
        itemsDpsACSalida.append(calculoDpsACSalida(lugar_instalacion, lugar_instalacion_opcion_techo_cubierta, tipoServicio,tensionServicio))
        #Calculo Interruptores automáticos AC (IAAC) (Circuito de salida inversor)
        interruptoresAutoSalidaInversor.append(calculoInterruptoresAutoSalidaInversor(tensionServicio,tipoServicio,inversor))
        #suma de las Corriente_Int de todos los campos FV, para Calculo Interruptores automáticos AC (IAAC) (Combinador AC )
        corriente=calculoCorriente_Int(tensionServicio,inversor)
        if (corriente !=None):
            sumCorriente_Int += corriente
        
        total_cadenas_paralelo=0
        for mppt in panelfv.mttps:
            cadenas_paralelo= mppt.numero_de_cadenas_en_paralelo
            cadenas_serie=mppt.numero_de_paneles_en_serie_por_cadena
            ##Datos nominales de mppt***************
            tension_Mpp= cadenas_serie  * vmmp_panel
            corrienteMPP= cadenas_paralelo * impp_panel
            tensionMaximaMppt= cadenas_serie * voc_panel * 1+(coef_voc_panel/100) * (temp_ambiente_mas_baja_esperada - 25  )
            ##***************************************
            max_conductoresFuente= mppt.cableado.input.maximo_numero_de_conductores
            max_conductoresSalida=mppt.cableado.output.maximo_numero_de_conductores
            distanciaConductorFuente= mppt.cableado.input.distancia_del_conductor_mas_largo
            distanciaConductorSalida= mppt.cableado.output.distancia_del_conductor_mas_largo
            tensionFuenteDiseno= mppt.cableado.input.caida_de_tension_de_diseno
            tensionSalidaDiseno= mppt.cableado.output.caida_de_tension_de_diseno
            tipo_alambradoEntrada=mppt.cableado.input.tipo_alambrado
            tipo_alambradoSalida=mppt.cableado.output.tipo_alambrado
            
            condutor=CalculoConductores(tem_amb,max_conductoresFuente,max_conductoresSalida,isc_panel,impp_panel,
                            cadenas_paralelo,distanciaConductorFuente,distanciaConductorSalida,corrienteMPP,tension_Mpp,
                            tensionFuenteDiseno,tensionSalidaDiseno,tipo_alambradoEntrada,tipo_alambradoSalida)
            conductoresMttp.append(condutor)    
            #Calculo de DPS DC FV.
            itemsDpsDC.append(seleccionItemDpsDC(tensionMaximaMppt,lugar_instalacion, lugar_instalacion_opcion_techo_cubierta,distanciaConductorSalida))
            #Calculo Interruptor manual DC (IMDC)
            itemInterruptorDC.append(seleccionIMDC(corrienteMPP,tensionMaximaMppt))
            #Calculo fusibles de cadena FV
            fusibles.append(calculoFusibles(cadenas_paralelo,isc_panel))
            #acumulado de las cadenas en paralelo de los mppts
            total_cadenas_paralelo +=cadenas_paralelo
            
            #añadiendo la caja combinatoria seleccionada para cada mppt
            cajasCombinadorasMppt.append(seleccionCajaCombinatoria2(cadenas_paralelo))
            
        #Calculo Interruptores automáticos AC (IAAC) (Combinador AC )
        #print "cadenas paralelo "+str(total_cadenas_paralelo)
        interruptoresAutoCombinador=calculoInterruptoresAutoCombinador(tensionServicio,tipoServicio,sumCorriente_Int)
        
        
        #calculo de conductores puesto a tierra AC
        conductorAC=calibreconductorAC(sumaIsal,tem_amb,max_conductCombinacionInversor,isc_panel,generalFv.fvs,tensionServicio)
        
        
        #calculo de cajas combitorias 
        cajaCombinatoriaGeneral=seleccionCajaCombinatoria1(total_cadenas_paralelo,len(panelfv.mttps))#una caja combinatoria para todo sloo mppts
        
        #Cajas combinatorias finales seleccionadas por cada panel fv
        cajasCombinadorasFinal.append(calculoFinalCajaCombinatorias(cajaCombinatoriaGeneral,cajasCombinadorasMppt))
    
    
    conductoresCombninacionInversor=CalculoConductorInversor(tipoServicio,sumaIsal,tem_amb,max_conductCombinacionInversor,isc_panel,
                                                        distanciaCombinacionInversor,tensionServicio,caidaTensionCombinacionInversor)
    
    #print dic_main.panelesSolares_dict[panel].isc
    print "conductores mppt"
    print conductoresMttp
    print "conductores inversor"
    print conductoresInversor
    print "conductorDC " + str(conductorDC)
    print "conductorAC "
    print conductorAC
    print "itemsDpsDC"
    print itemsDpsDC
    print "itemInterruptorDC"
    print itemInterruptorDC
    print "itemsDpsACSalida"
    print itemsDpsACSalida
    print "itemDpsACInyeccion "+itemDpsACInyeccion
    print "fusibles"
    print fusibles
    print "calculoInterruptoresAutoSalidaInversor"
    print interruptoresAutoSalidaInversor
    print "calculoInterruptoresAutoCombinador"
    print interruptoresAutoCombinador
    print "cajasCombinadorasFinal"
    for x in aplanarList(cajasCombinadorasFinal):
        print x.descripcion
    #print cajasCombinadorasFinal
    print "paneles_agrupados"
    print paneles_agrupados
    print "conductoresCombninacionInversor "+  str (conductoresCombninacionInversor)
    

""" 
#funcion que suma todos los Isal_max de la base de datos del inversor segun el inversor seleccionado  
def sumIsal(inversor):
    dic_main=mainInfoLib.getDic() #diccionario principal con los datos cargados de excel
    isal_max_1=float(dic_main.inversores_dict[inversor].isal_max_1)
    isal_max_2=float(dic_main.inversores_dict[inversor].isal_max_2)
    isal_max_3=float(dic_main.inversores_dict[inversor].isal_max_3)
    return isal_max_1+isal_max_1+isal_max_1
"""
    
def cotizador(request):
    return render(request, 'formulario.html')
    
    
    
def calculos(request):
    seleccionCalibre(30,10,4,9.82,8.28,4,500,200,33.12,92.4,20,20,'','')
    return HttpResponse("hola")
    
def aplanarList(l):
    ret = []
    for i in l:
        if isinstance(i, list) or isinstance(i, tuple):
            ret.extend(aplanarList(i)) #aplanarList() siendo usado dentro de def aplanarList()
        else:
            ret.append(i)
    return ret