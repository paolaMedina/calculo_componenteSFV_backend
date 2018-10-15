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
from lib.calculo_conductores import *  
from objetos_nativos_python_frontend import Generalfv
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.views.generic import View
from datetime import date
from lib.render import render_to_pdf
#import requests
from threading import Thread, activeCount
import json
from django.contrib.auth.decorators import login_required
from simulador.utilities import *
from django.core.mail import EmailMessage
from lib.render import render_to_file



class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening
         
# Realiza la  serialización de los archivos CSV, ante peticion get de la api
class DataCsvView(APIView):
    def get(self, request, format=None):
        serializer = DataSerializer(mainInfoLib.getData())
        return Response(serializer.data)
        
        
#recibir el json de la api y realizar operaciones
class deserializacion (APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    @csrf_exempt
    def post(self, request, format=None):
        serializer = GeneralFVSerializer(data=request.data)
        if serializer.is_valid():
            print "valido"
            #print  serializer.validated_data
            generalFv=getGeneralFvNativeObject(serializer.data)
            lectura(generalFv)
            #messages.success(self.request, "Cotizacion")
            data = {
            'today': timezone.now(), 
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
            
            }
            pdf = render_to_pdf('pdf.html', data)
            return HttpResponse(pdf, content_type='application/pdf', status=303)
            #return  HttpResponseRedirect('pdf')
        else:
            print serializer.data
            print serializer.errors
            return Response(serializer.errors,  status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#recibir el json de la api y realizar operaciones
class deserializacion2 (APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    @csrf_exempt
    def post(self, request, format=None):
        print request.data
        if( request.data.get('validated_data')):
            print "valido"
            generalFv = perfect_information_posted(request)
            data = lectura(generalFv)
            #print data
            filename="cotizacion_"+data['proyecto']
            if (request.user.groups.all()[0].name=="administrador"):
                print "admin"
                file = render_to_file('pdf_admin.html', data,filename)
            else:
                print "otro"
                file = render_to_file('pdf.html', data,filename)
            return Response(status=200)
        else:
            serializer = GeneralFVSerializer(data=request.data)
            print "serializador"
            
           
            if serializer.is_valid():
                return Response(serializer.data,  status=200)
            else:
                print "invalido"
                print serializer.errors
                return Response(serializer.errors,  status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
def perfect_information_posted(request):
    information_posted_string = request.data.get('validated_data')
    #print(information_posted_string)
    information_posted_json = json.loads(information_posted_string)
    serializer = GeneralFVSerializer(data=information_posted_json)
    generalFv = {}
    if(serializer.is_valid()):
        #print(serializer.data)
        generalFv=getGeneralFvNativeObject(serializer.data)
    else:
        return Response(serializer.errors,  status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return generalFv
def getGeneralFvNativeObject(serializer):
    generalfv=Generalfv(serializer['potencia_de_planta_fv'],serializer['nombre_proyecto'],serializer['temperatura_ambiente'],
    serializer['minima_temperatura_ambiente_esperada'],serializer['tipo_de_inversor'],
    serializer['lugar_instalacion_opcion_techo_cubierta'],serializer['tipo_servicio'],serializer['voltage_servicio'],
    serializer['lugar_instalacion'],serializer['combinacion_inversor'],serializer['fvs'])
    mttps= generalfv.fvs[0].mttps
    return generalfv
def lectura(generalFv):
    dic_main=mainInfoLib.getDic() #diccionario principal con los datos cargados de excel
    conductoresMttp=[]#matriz de los calibres de entrada y salida de los mppts
    conductoresInversor=[] #matriz de los calibres de entrada y salida de los inversores de campos fv
    conductoresDC=[]#arreglo para los  conductores  puesta a tierra DC
    itemsDpsDC_mppt=[]#arreglo con los dps DC de cada mppt, sin validar si existen repetidos
    itemInterruptorDC=[]
    itemsDpsACSalida=[]
    fusibles=[]
    interruptoresAutoSalidaInversor=[]
    sumCorriente_Int=0
    sumaIsal=0
    inversoresSeleccionados=[]
    
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
    
        #calculo de conductores para salida inversor
        inversor=panelfv.modelo_panel_solar_2#modelo del inversor
        isalInversor=isalN(inversor,tensionServicio)
        sumaIsal+=isalInversor#acumulado de los isal de cada salida inversor
        conductorInversor= CalculoConductorInversor(panelfv.salida_inversor.output,tipoServicio,isalInversor,tem_amb,isc_panel,tensionServicio)
        conductoresInversor.append(conductorInversor)
        
        #calculo de conductores puesto a tierra DC
        conductoresDC.append(calibreconductorDC(panelfv.mttps,isc_panel))
        
        inversoresSeleccionados.append(inversor)#acumulando los inversores seleccionados
        
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
            distanciaConductorSalida= mppt.cableado.output.distancia_del_conductor_mas_largo
            
            #calculo de conductores de entrada y salida de mppts
            condutor=CalculoConductores(tem_amb,mppt,isc_panel,impp_panel,corrienteMPP,tension_Mpp)
            conductoresMttp.extend(condutor)    
            #Calculo de DPS DC FV.
            itemsDpsDC_mppt.extend(seleccionItemDpsDC(tensionMaximaMppt,lugar_instalacion, lugar_instalacion_opcion_techo_cubierta,distanciaConductorSalida))
            #Calculo Interruptor manual DC (IMDC)
            itemInterruptorDC.append(seleccionIMDC(corrienteMPP,tensionMaximaMppt))
            #Calculo fusibles de cadena FV
            fusibles.extend(calculoFusibles(cadenas_paralelo,isc_panel))
            #acumulado de las cadenas en paralelo de los mppts
            total_cadenas_paralelo +=cadenas_paralelo
            
            #añadiendo la caja combinatoria seleccionada para cada mppt
            cajasCombinadorasMppt.append(seleccionCajaCombinatoria2(cadenas_paralelo))
            
        #Calculo Interruptores automáticos AC (IAAC) (Combinador AC )
        #print "cadenas paralelo "+str(total_cadenas_paralelo)
        interruptoresAutoCombinador=calculoInterruptoresAutoCombinador(tensionServicio,tipoServicio,sumCorriente_Int)
        
        
        #calculo de conductores puesto a tierra AC
        conductorAC=calibreconductorAC(sumaIsal,tem_amb,max_conductCombinacionInversor,distanciaCombinacionInversor,isc_panel,generalFv.fvs,tensionServicio)
        
        
        #calculo de cajas combitorias 
        cajaCombinatoriaGeneral=seleccionCajaCombinatoria1(total_cadenas_paralelo,len(panelfv.mttps))#una caja combinatoria para todo sloo mppts
        
        #Cajas combinatorias finales seleccionadas por cada panel fv
        cajasCombinadorasFinal.extend(calculoFinalCajaCombinatorias(cajaCombinatoriaGeneral,cajasCombinadorasMppt))
   
    canalizaciones=calculoCanalizacion(generalFv.fvs, generalFv.combinacion_inversor)
    #con los items dps que se seleccionaron en cada mttp, se verifica si no existen mas de dos dps iguales, si los hay se unen 
    ItemsDpsDCCombinados=combinarItems(itemsDpsDC_mppt)
    itemInterruptorDCCombinados=combinarItems(itemInterruptorDC)
    itemsDpsACSalidaCombinados=combinarItems(itemsDpsACSalida)
    fusiblesCombinados=combinarItems(fusibles)
    interruptoresAutoSalidaInversorCombinados=combinarItems(interruptoresAutoSalidaInversor)
    cajasCombinadorasFinalCombinados=combinarItems(cajasCombinadorasFinal) 
    inversores=calculoInversores(inversoresSeleccionados)
    conductoresCombninacionInversor=CalculoConductorInversor(generalFv.combinacion_inversor.input,tipoServicio,sumaIsal,tem_amb,isc_panel,tensionServicio)
    conductores=calculoConductoresFinal(conductoresMttp,conductoresInversor,conductoresCombninacionInversor)
    
    #añadir un index a cada objeto
    counter = Counter(1) 
    total = Total() 
    #reducir tamaño de la potencia
    potencia=generalFv.potencia_de_planta_fv[:generalFv.potencia_de_planta_fv.find(".")+4]
    data = {
        'today': date.today(), 
        'proyecto':generalFv.nombre_proyecto,
        'potencia':potencia,
        'conductores': add_Index_Cost(conductores, counter,total),
        'canalizaciones': add_Index_Cost(canalizaciones,counter,total),
        'conductoresDC': add_Index_Cost(conductoresDC,counter,total),
        'conductoresAC':add_Index_Cost(conductorAC,counter,total),
        'itemsDpsDC': add_Index_Cost(ItemsDpsDCCombinados,counter,total),
        'itemInterruptorDC':add_Index_Cost(itemInterruptorDCCombinados,counter,total),
        'itemsDpsACSalida':add_Index_Cost(itemsDpsACSalidaCombinados,counter,total),
        'itemDpsACInyeccion':add_Index_Cost([itemDpsACInyeccion],counter,total),
        'fusibles':add_Index_Cost(fusiblesCombinados,counter,total),
        'interruptoresAutoSalidaInversor': add_Index_Cost(interruptoresAutoSalidaInversorCombinados,counter,total),
        'interruptorAutoCombinador':add_Index_Cost([interruptoresAutoCombinador],counter,total),
        'CombinadorasFinal': add_Index_Cost(cajasCombinadorasFinalCombinados,counter,total),
        'paneles':add_Index_Cost(paneles_agrupados,counter,total),
        'inversores':add_Index_Cost(inversores,counter,total),
        'total':total
        
        }
    return data
    
@login_required    
def cotizador(request):
    return render(request, 'formulario.html')
def GeneratePdf(request,data):
    file = render_to_pdf('pdf.html', data)
    response = HttpResponse(file, content_type='application/pdf')
    #send_email(file)
    return response
    

@login_required
def viewSendPDF (request,filename):
    #print filename
    if request.method == "GET":
        contexto = {'pdf':"/media/cotizaciones/"+filename+".pdf"}
        return render(request,'prueba.html', contexto )
    
    if request.method == "POST":
        destinatarios=request.POST['emails'].split(";")
        print destinatarios
        send_email(destinatarios,filename)
        #contexto = {'pdf':"/media/cotizaciones/"+filename}
        return HttpResponseRedirect (reverse ('cotizadorFv:cotizacion'))


def send_email(destinatarios,filename):
    route="media/cotizaciones/"+filename+".pdf"
    file = open(route, "rb")
    filename=filename+".pdf"
    print filename
    msg = EmailMessage('Cotización calculadora fotovoltaica-Soler', '', 'angiepmc93@gmail.com',destinatarios)
    msg.content_subtype = "html"  
    msg.attach(filename, file.read() , 'application/pdf')
    msg.send()
    

@csrf_exempt        
def alonePdf(request):
    print request
    if request.method == "POST":
        print "post"
        generalFv = request.data
        data = lectura(generalFv)
        filename="cotizacion_"+data['proyecto']
        file = render_to_file('pdf.html', data,filename)
        return Response(status=200)
    if request.method == "GET":
        return render_to_pdf('pdf.html',{})
        
      
      
class Total:
    def __init__(self):
        self.value = 0
    def add(self,monto):
        self.value += monto
        
"""
Agregar contador a los elementos de la cotización
"""
class Counter:
    def __init__(self, start):
        self.index = start
    def increment(self):
        self.index += 1

def add_Index_Cost(list, counter,total):
    for element in list:
        element.index = counter.index
        counter.increment()
        total.add(element.valor_total)
    return list
