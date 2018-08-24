# -*- coding: utf-8 -*-

from . import constants
from cotizadorFV.modelsCSV import *
from cotizadorFV.models import CalibreConductor,Resultado
from cotizadorFV.lib import lib as mainInfoLib
import math
from unidecode import unidecode

correcion_tem_amb= constants.correcion_tem_amb
factorAjusteConductores=constants.factorAjusteConductores
calibre=constants.calibre
area_calibre=constants.area_calibre
calibreConductor=constants.calibreConductor
calibreAire=constants.calibreAire


#funcion que determina el Isal_max de la base de datos inversores dependiendo inversor y el Vsal seleccionado en la cotización  
def isalN(inversor,tensionServicio):
    dic_main=mainInfoLib.getDic() #diccionario principal con los datos cargados de excel
    isal=0
    isal_max_1=float(dic_main.inversores_dict[inversor].isal_max_1)
    
    isal_max_2=float(dic_main.inversores_dict[inversor].isal_max_2)
    isal_max_3=float(dic_main.inversores_dict[inversor].isal_max_3)
    if tensionServicio==float(dic_main.inversores_dict[inversor].vsal_1):
        isal=isal_max_1
    elif tensionServicio==float(dic_main.inversores_dict[inversor].vsal_2):
        isal=isal_max_2
    elif tensionServicio==float(dic_main.inversores_dict[inversor].vsal_3):
        isal=isal_max_3
    return isal

def aplanarList(l):
    ret = []
    for i in l:
        if isinstance(i, list) or isinstance(i, tuple):
            ret.extend(aplanarList(i)) #aplanarList() siendo usado dentro de def aplanarList()
        else:
            ret.append(i)
    return ret
    
#kt
def correcionTemp(tem_amb):
    kt=0
    for i in range(len(correcion_tem_amb)):
      if (correcion_tem_amb[i][0]<=tem_amb<=correcion_tem_amb[i][1]):
          kt=correcion_tem_amb[i][2]
          break 
    return kt

#kr        
def factorLlenado(max_conductores):
    kr=0
    if max_conductores<=3:
        kr=1
    else:
        for i in range(len(factorAjusteConductores)):
          if (factorAjusteConductores[i][0]<=max_conductores<=factorAjusteConductores[i][1]):
              kr=factorAjusteConductores[i][2]/100.0
              break
    return kr
    
def calculo_caidaTension(i,l,s,v):
    """
    print "i "+ str(i)
    print "l " +str(l)
    print "s "+ str(s)
    print "v " +str(v)"""
    r=44
    caida_tension=((2*i*l)/(r*s*v))*100
    return caida_tension

def seleccionarConductor(calibre):
    conductor_seleccionado=0
    for i in range(len(area_calibre)):
        if (calibre==area_calibre[i][0]):
            conductor_seleccionado=area_calibre[i][1]
            break
    return conductor_seleccionado
    
#funcion que dependiendo el tipo de alambrado devuelve la posicion del calibre que se selecciona
def posicionCalibre(corr_nominal,tipo_alambrado):
    posicion=0
    if (tipo_alambrado !='Al aire libre'):
        for i in range(len(calibre)):
            if (corr_nominal<=calibre[i][1]):
                posicion=i
                break
    else: 
        for i in range(len(calibreAire)):
            if (corr_nominal<=calibreAire[i][1]):
                posicion=i
                break
    return posicion
#_________________________________________________CIRCUITO DE FUENTE FV_____________________________________________


def corrienteNominalEntrada(tem_amb,max_conductores,isc_panel):
    kt=correcionTemp(tem_amb)
    kr=factorLlenado(max_conductores)
    
    return isc_panel*(1.56/(kt*kr)) 
    

def posicionCalibreFuente(tem_amb,max_conductores,isc_panel,tipo_alambrado):
    
    corr_nominal=corrienteNominalEntrada(tem_amb,max_conductores,isc_panel)
    posicion=posicionCalibre(corr_nominal,tipo_alambrado)
    return posicion
        

#caida de tension en la fuente

def caidaTensionFuente(posicionCalibre,tension_Mpp,impp_panel,distanciaConductor):
   
    calibre_seleccionado=calibre[posicionCalibre][0]
    conductor_seleccionado=seleccionarConductor(calibre_seleccionado)
    caida_tension=calculo_caidaTension(impp_panel,distanciaConductor,conductor_seleccionado,tension_Mpp)
    return caida_tension
    
    

#________________________________________________CIRCUITO DE SALIDA FV_____________________________________________



def corrienteNominalSalida(tem_amb,max_conductores,isc_panel,cadenas_paralelo):
    kt=correcionTemp(tem_amb)
    #print "kt salida"+str(kt)
    kr=factorLlenado(max_conductores)
    #print "kr salida"+str(kr)
    i=cadenas_paralelo*isc_panel*1.56
    corrienteNom=i/(kt*kr)
    return  corrienteNom
    
    
def posicionCalibreSalida(tem_amb,max_conductores,isc_panel,cadenas_paralelo,tipo_alambrado):
    corr_nominal=corrienteNominalSalida(tem_amb,max_conductores,isc_panel,cadenas_paralelo)
    posicion=posicionCalibre(corr_nominal,tipo_alambrado)
    return posicion
    

def caidaTensionSalida(posicionCalibre,distanciaConductor,corrienteMPP,tension_Mpp):
    calibreSeleccionado=calibre[posicionCalibre][0]
    conductor_seleccionado=seleccionarConductor(calibreSeleccionado)
    caida_tension=calculo_caidaTension(corrienteMPP,distanciaConductor,conductor_seleccionado,tension_Mpp)
    return caida_tension
    

 #_______________________________________________________________________________________________
    
#Seleccionar el calibre que cumple con la tension ingresada por el usuario

def CalculoConductores(tem_amb,mppt,isc_panel,impp_panel,corrienteMPP,tension_Mpp):
    cadenas_paralelo= mppt.numero_de_cadenas_en_paralelo
    max_conductoresFuente= mppt.cableado.input.maximo_numero_de_conductores
    max_conductoresSalida=mppt.cableado.output.maximo_numero_de_conductores
    distanciaConductorFuente= mppt.cableado.input.distancia_del_conductor_mas_largo
    distanciaConductorSalida= mppt.cableado.output.distancia_del_conductor_mas_largo
    tensionFuenteDiseno= mppt.cableado.input.caida_de_tension_de_diseno
    tensionSalidaDiseno= mppt.cableado.output.caida_de_tension_de_diseno
    tipo_alambradoEntrada=mppt.cableado.input.tipo_alambrado
    tipo_alambradoSalida=mppt.cableado.output.tipo_alambrado
    #caida de tension fuente inicial                    
    posCalibreFuente=posicionCalibreFuente(tem_amb,max_conductoresFuente,isc_panel,tipo_alambradoEntrada)
    caidaTensionF=caidaTensionFuente(posCalibreFuente,tension_Mpp,impp_panel,distanciaConductorFuente)
    #caida de tension salida inicial                    
    posCalibreSalida=posicionCalibreSalida(tem_amb,max_conductoresSalida,isc_panel,cadenas_paralelo,tipo_alambradoSalida)
    caidaTensionS=caidaTensionSalida(posCalibreSalida,distanciaConductorSalida,corrienteMPP,tension_Mpp)
    
    
    
    suma_caida_tension_diseno=tensionFuenteDiseno+tensionSalidaDiseno
    for i in range(len(calibre)):
        suma_caida_tension=caidaTensionF+caidaTensionS
        if (suma_caida_tension>suma_caida_tension_diseno):
            if (caidaTensionF>caidaTensionS):
                posCalibreFuente +=1
                caidaTensionF=caidaTensionFuente(posCalibreFuente,tension_Mpp,impp_panel,distanciaConductorFuente)
            else:
                posCalibreSalida +=1
                caidaTensionS=caidaTensionSalida(posicionCalibreSalida,distanciaConductorSalida,corrienteMPP,tension_Mpp)
        else: 
            break
                
    distanciaFuente=distanciaConductorFuente*2
    calibreFuente=calibre[posCalibreFuente][0]
    
    distanciaSalida=distanciaConductorSalida*2
    calibreSalida=calibre[posCalibreSalida][0]
    
    calibreSeleccionadoFuente=CalibreConductor()
    calibreSeleccionadoFuente.tipo_conductor=mppt.cableado.input.tipo_conductor
    calibreSeleccionadoFuente.material_conductor=mppt.cableado.input.material_conductor
    calibreSeleccionadoFuente.calibre=calibreFuente
    calibreSeleccionadoFuente.distancia=distanciaFuente
  
    calibreSeleccionadoSalida=CalibreConductor()
    calibreSeleccionadoSalida.tipo_conductor=mppt.cableado.output.tipo_conductor
    calibreSeleccionadoSalida.material_conductor=mppt.cableado.output.material_conductor
    calibreSeleccionadoSalida.calibre=calibreSalida
    calibreSeleccionadoSalida.distancia=distanciaSalida
    
    calibresES=[calibreSeleccionadoFuente,calibreSeleccionadoSalida]
    return calibresES
    
    
    
#___________________________________________Salida Inversor y combinacion inversor___________________________________________________---


def corrienteNominalInversor(isal,tem_amb,max_conductores,isc_panel):
    kt=correcionTemp(tem_amb)
    kr=factorLlenado(max_conductores)
    return (isal*1.25)/(kt*kr)
    

def posicionCalibreInversor(isal,tem_amb,max_conductores,isc_panel):
    
    posicion=0
    corr_nominal=corrienteNominalInversor(isal,tem_amb,max_conductores,isc_panel)
    for i in range(len(calibre)):
        if (corr_nominal<=calibre[i][1]):
            posicion=i
            break
    return posicion
    

def caidaTensionInversor(tipo_servicio,posicionCalibre,isal,tem_amb,max_conductores,isc_panel,l,v):
    cos=1
    r=44
    calibreSeleccionado=calibre[posicionCalibre][0]
    s=seleccionarConductor(calibreSeleccionado)#conductor_seleccionado
    i=corrienteNominalInversor(isal,tem_amb,max_conductores,isc_panel)#corriente nominal salida
    if (tipo_servicio.encode('utf8')==u"Monofásica".encode('utf8')):
        factor=2
    else :
        factor =1
    caida_tension= factor*(i*l*cos)/(r*s)*100/v
    
    return caida_tension

#funcion que entrega el  calibre salida para el inversor  y  tambien se usa para circuito de inversor combinadoo (isal=suma de los isal de los inversore)
   
def CalculoConductorInversor(cableadoInversor,tipo_servicio,isal,tem_amb,isc_panel,tensionServicio):    
    conductoresInversor=None
    max_conductores=cableadoInversor.maximo_numero_de_conductores
    distanciaConductor=cableadoInversor.distancia_del_conductor_mas_largo
    caidaTensionUsuario=cableadoInversor.caida_de_tension_de_diseno

    posicionCalibreSalida=posicionCalibreInversor(isal,tem_amb,max_conductores,isc_panel)
    caidaTensionSalida=caidaTensionInversor(tipo_servicio,posicionCalibreSalida,isal,tem_amb,max_conductores,isc_panel,distanciaConductor,tensionServicio)
    
    for i in range(len(calibre)):
        if (caidaTensionSalida>caidaTensionUsuario):
                posicionCalibreSalida +=1
                caidaTensionSalida=caidaTensionInversor(tipo_servicio,posicionCalibreSalida,isal,tem_amb,max_conductores,isc_panel,distanciaConductor,tensionServicio)
        else: 
            break
    
    if (tipo_servicio.encode('utf8')==u"Monofásica".encode('utf8')):
        distancia=distanciaConductor*2
    else:
        distancia=distanciaConductor*4
        
    calibreSeleccionado=calibre[posicionCalibreSalida][0]
    
    conductoresInversor=CalibreConductor()
    conductoresInversor.tipo_conductor=cableadoInversor.tipo_conductor
    conductoresInversor.material_conductor=cableadoInversor.material_conductor
    conductoresInversor.calibre=calibreSeleccionado
    conductoresInversor.distancia=distancia
    return conductoresInversor
                
    
#____________________Calibre conductores puesto a Tierra

#funcion aux para seleccionar el calibre segun la tabla calibreConductor para conductores
def buscarCalibreCondutor(corrienteNominal):
    for i in range(len(calibreConductor)):
        if (corrienteNominal<=calibreConductor[i][0]):
            conductor_seleccionado=calibreConductor[i][1]
            break
    return conductor_seleccionado


#Calibre de conductor puesta a tierra DC
def calibreconductorDC(mttps,Isc_panel):
    corrienteNominal=0 #corriente nominal del circuito de la salida fotovoltaica 
    conductor_seleccionado=0
    for mttp in mttps:
        corrienteNominal += mttp.numero_de_cadenas_en_paralelo* Isc_panel*1.56
    #buscar el calibre del conductor equivalente  a la tabla
    conductor_seleccionado=buscarCalibreCondutor(corrienteNominal)
        
    return conductor_seleccionado
    
    

#Calibre de conductor puesta a tierra AC
def calibreconductorAC(sumaIsal,tem_amb,max_conductCombinacionInversor,isc_panel,camposFV,tensionServicio):
    list=[]
    corrienteCombinacionInversor=corrienteNominalInversor(sumaIsal,tem_amb,max_conductCombinacionInversor,isc_panel)
    calibreCombinacionInversor=buscarCalibreCondutor(corrienteCombinacionInversor)
    for campoFV in camposFV:
        isalInversor=isalN(campoFV.modelo_panel_solar_2,tensionServicio)
        max_conductInversor=campoFV.salida_inversor.output.maximo_numero_de_conductores
        corrienteInversor=corrienteNominalInversor(isalInversor,tem_amb,max_conductInversor,isc_panel)
        calibreInversor=buscarCalibreCondutor(corrienteInversor)
        list.append(calibreInversor)
        list.append(calibreCombinacionInversor)
    return list
    

#__________________________________DPS FV______________________

def cantidadMppt(distanciaConductorSalida):
    cantidad=0
    if (distanciaConductorSalida<10):
        cantidad=1
    else:
        cantidad=2
    return cantidad
    
def tipoDps(tipoDps,lugar_instalacion, lugar_instalacion_opcion_techo_cubierta):
    tipo=""
    if lugar_instalacion=='Suelo':
        tipo="2"
    else:
        if (lugar_instalacion_opcion_techo_cubierta=="Caso A") or (lugar_instalacion_opcion_techo_cubierta=="Caso B"):
            tipo="2"
        else: 
            if (tipoDps=="dpsDC"): tipo="1+2"
            elif(tipoDps=="dpsAC"): tipo="1"
        
    return tipo


def seleccionItemDpsDC(tensionMaximaMppt,lugar_instalacion, lugar_instalacion_opcion_techo_cubierta,distanciaConductorSalida):
    dic_main=mainInfoLib.getDic()
    items=[]
    numItems=cantidadMppt(distanciaConductorSalida)
    tipo=tipoDps("dpsDC",lugar_instalacion, lugar_instalacion_opcion_techo_cubierta)
    
    filtroDps = { clave: valor for clave, valor in dic_main.dpsDC_dict.items() if valor.tipo == tipo}
    dpsDC_list_sorted =  sorted(filtroDps.values(), key=DpsDC.getSortKey)
    for dps in dpsDC_list_sorted:
        if (tensionMaximaMppt<dps.uc):
            item=dps.descripcion
            if (numItems==2):
                items=[item,item]
            else:items=[item]
            break
    return items
 
#Calculo Interruptor manual DC (IMDC)
def seleccionIMDC(corrienteMpp,tensionMaximaMppt):
    interruptorTension=None
    interruptorIth=None
    dic_main=mainInfoLib.getDic()
    filtroInterruptores = { clave: valor for clave, valor in dic_main.interruptoresManuales_dict.items() if valor.no_contactos == 2}
    interruptores_list_sortedTension =  sorted(filtroInterruptores.values(), key=InterruptorManual.getSortTension)
    
    #sacando la mejor opcion entre precio y tension
    listResultanteTension=[]
    for i in range(0,len(interruptores_list_sortedTension)) :
        if (tensionMaximaMppt<interruptores_list_sortedTension[i].tension)and (corrienteMpp<interruptores_list_sortedTension[i].ith):
            interruptorTension=interruptores_list_sortedTension[i]
            listResultanteTension=interruptores_list_sortedTension[i:]
            break
    
    #probar si hay empate en tension (si hay otro item con la misma tension)       
    for i in range(0,len(listResultanteTension)-1) :
        
        if listResultanteTension[i].tension==listResultanteTension[i+1].tension:
            if listResultanteTension[i].precio > listResultanteTension[i+1].precio:
                interruptorTension=listResultanteTension[i+1]
                
        else: break
           
    #sacando la mejor opcion entre precio y ith       
    listResultanteIth=[]
    interruptores_list_sortedIth =  sorted(filtroInterruptores.values(), key=InterruptorManual.getSortIth)    
    for i in range(0,len(interruptores_list_sortedIth)):
        if (corrienteMpp<interruptores_list_sortedIth[i].ith) and (tensionMaximaMppt<interruptores_list_sortedIth[i].tension):
            interruptorIth=interruptores_list_sortedIth[i]
            listResultanteIth=interruptores_list_sortedIth[i:]
            break
        
    #probar si hay empate en ith (si hay otro item con el mismo ith)       
    for i in range(0,len(listResultanteIth)-1) :
        
        if listResultanteIth[i].ith==listResultanteIth[i+1].ith:
            if listResultanteIth[i].precio > listResultanteIth[i+1].precio:
                interruptorIth=listResultanteIth[i+1]
        else: break
    
    #escoger le mejoro entre los items seleccionados anteriormente de tension y ith    
    if (interruptorTension!=None and interruptorIth !=None):   
        if (interruptorTension.precio>interruptorIth.precio):
            item=interruptorIth.descripcion
        else:
            item=interruptorTension.descripcion
    else: item=None
    
    return item
   
def cantPolos(tipo,tipoServicio):
    polos=None
    if (tipoServicio.encode('utf8')==u"Monofásica".encode('utf8')):
        polos=2
    else: 
        if (tipo=="dps"): polos=4
        else: polos=3
    return polos
    
def nivelTension(tipoServicio,tensionServicio):
    nivel_tension=None
    if (tipoServicio.encode('utf8')==u"Monofásica".encode('utf8')):
        nivel_tension= tensionServicio
    else: 
        nivel_tension= tensionServicio/math.sqrt(3)
    return nivel_tension   
    
def tipoDpsACInyeccion(lugar_instalacion, lugar_instalacion_opcion_techo_cubierta):
    tipo=None
    if lugar_instalacion=='Suelo':
        tipo="1"
    else:
        if (lugar_instalacion_opcion_techo_cubierta=="Caso C") or (lugar_instalacion_opcion_techo_cubierta=="Caso B"):
            tipo="1"
        else: tipo="2"
        
    return tipo

#calculo de DPS AC generico 
def calculoDpsACGeneral(tipo,polos,nivel_tension):
    dic_main=mainInfoLib.getDic()
    dpsAC=None
    
    filtroTipo = { clave: valor for clave, valor in dic_main.dpsAC_dict.items() if valor.tipo == int(tipo)}
    filtroPolo= { clave: valor for clave, valor in filtroTipo.items() if valor.no_polos == polos}
    DpsAC_list_sortedUc =  sorted(filtroPolo.values(), key=DpsAC.getSortUc)
    listResultante=[]
    for i in range(0,len(DpsAC_list_sortedUc)) :
        if (nivel_tension<DpsAC_list_sortedUc[i].uc):
            dpsAC=DpsAC_list_sortedUc[i].descripcion
            listResultante=DpsAC_list_sortedUc[i:]
            break
            
     #probar si hay empate (si hay otro item con el mismo uc)       
    for i in range(0,len(listResultante)-1) :
        if listResultante[i].uc==listResultante[i+1].uc:
            if listResultante[i].in_in < listResultante[i+1].in_in:
                dpsAC=listResultante[i+1].descripcion
        else: break
    
    return dpsAC
    
    
#Calculo DPS AC (Salida inversores)
def calculoDpsACSalida(lugar_instalacion, lugar_instalacion_opcion_techo_cubierta, tipoServicio,tensionServicio):
    
    tipo=tipoDps("dpsAC",lugar_instalacion, lugar_instalacion_opcion_techo_cubierta)
    polos=cantPolos("dps",tipoServicio)
    nivel_tension=nivelTension(tipoServicio,tensionServicio)
    dpsAC=calculoDpsACGeneral(tipo,polos,nivel_tension)
        
    return dpsAC



#Calculo  DPS AC (Inyección)
def calculoDpsACInyeccion(lugar_instalacion, lugar_instalacion_opcion_techo_cubierta, tipoServicio,tensionServicio):
    tipo=tipoDpsACInyeccion(lugar_instalacion, lugar_instalacion_opcion_techo_cubierta)
    polos=cantPolos("dps",tipoServicio)
    nivel_tension=nivelTension(tipoServicio,tensionServicio)
    dpsAC=calculoDpsACGeneral(tipo,polos,nivel_tension)
        
    return dpsAC


#Calculo fusibles de cadena FV
def calculoFusibles(cadenas_paralelo,iscPanel):
    dic_main=mainInfoLib.getDic()
    fusible=None
    fusibles=[]
    corrienteIn=In=1.5625*iscPanel
    cantidadMPPT= 0
    if cadenas_paralelo > 2 :
       
        cantidadMPPT=cadenas_paralelo*2
    
    
    fusibles_list_sortedUc =  sorted(dic_main.fusible_dict.values(), key=Fusible.getSortKeyIn)
    for fusible in fusibles_list_sortedUc:
        if (corrienteIn<fusible.in_in):
            fusible=fusible.descripcion
            break
            
    if cantidadMPPT !=0 and fusible !=None:
        for i in range(0,cantidadMPPT):
            fusibles.append(fusible)
    return fusibles


def calculoCorriente_Int(tensionServicio,inversor):
    dic_main=mainInfoLib.getDic()
    corriente=None
    i_int_sal_1=float(dic_main.inversores_dict[inversor].i_int_sal_1)
    i_int_sal_2=float(dic_main.inversores_dict[inversor].i_int_sal_2)
    i_int_sal_3=float(dic_main.inversores_dict[inversor].i_int_sal_3)
    if tensionServicio==float(dic_main.inversores_dict[inversor].vsal_1):
        corriente=i_int_sal_1
    elif tensionServicio==float(dic_main.inversores_dict[inversor].vsal_2):
        corriente=i_int_sal_2
    elif tensionServicio==float(dic_main.inversores_dict[inversor].vsal_3):
        corriente=i_int_sal_3
        
    return corriente

def calculoInterruptoresAutoGeneral(polos,corriente_Int,tensionServicio):
    interruptor=None
    listResultante=[]
    dic_main=mainInfoLib.getDic()
    filtroPolo= { clave: valor for clave, valor in dic_main.interruptoresAuto_dict.items() if valor.no_polos == polos}
    filtroTension= { clave: valor for clave, valor in filtroPolo.items() if  tensionServicio <=valor.tension or tensionServicio <=valor.tension_2 }
    interruptor_list_sortedIn =  sorted(filtroTension.values(), key=InteAuto.getSortKeyIn)
    
            
    for i in range(0,len(interruptor_list_sortedIn)) :
        if (corriente_Int<=interruptor_list_sortedIn[i].in_in):
              
            interruptor=interruptor_list_sortedIn[i].descripcion
            listResultante=interruptor_list_sortedIn[i:]
            
            break
    ##comparar si hay empate        
    for i in range(0,len(listResultante)-1) :
        if listResultante[i].in_in==listResultante[i+1].in_in:
            if listResultante[i].icn < listResultante[i+1].icn:
                interruptor=listResultante[i+1].descripcion
        else: break
    return interruptor
    


def calculoInterruptoresAutoCombinados(tensionServicio,tipoServicio,inversor):
    polos=cantPolos("interruptores",tipoServicio)
    corriente_Int = calculoCorriente_Int(tensionServicio,inversor)
    interruptor=calculoInterruptoresAutoGeneral(polos,corriente_Int,tensionServicio)
    return interruptor
    

def calculoInterruptoresAutoSalidaInversor(tensionServicio,tipoServicio,inversor):
    polos=cantPolos("interruptores",tipoServicio)
    corriente_Int = calculoCorriente_Int(tensionServicio,inversor)
    interruptor=calculoInterruptoresAutoGeneral(polos,corriente_Int,tensionServicio)
    return interruptor
    
def calculoInterruptoresAutoCombinador(tensionServicio,tipoServicio,corriente_Int):
    polos=cantPolos("interruptores",tipoServicio)
    interruptor=calculoInterruptoresAutoGeneral(polos,corriente_Int,tensionServicio)
    return interruptor
  
#Armario que soporte la cantidad total de cadenas en paralelo y MPPTs del campo FV  y con menor precio
def seleccionCajaCombinatoria1(total_cadenas_paralelo,total_mppts):
    seleccion=None
    dic_main=mainInfoLib.getDic()
    filtro1= { clave: valor for clave, valor in dic_main.armarios_dict.items() if 
                (valor.capacidad_cadenas >= total_cadenas_paralelo) and(valor.capacidad_mppts >= total_mppts) }
                
    if len(filtro1)>0:
        armarios_list_sortedPrecio =  sorted(filtro1.values(), key=Armario.getSortKeyPrecio)
        seleccion=armarios_list_sortedPrecio[0]
    return seleccion
    
#Un armario para cada MPPT que soporte la cantidad de cadenas de dicho MPPT
def seleccionCajaCombinatoria2(cadenas_paralelo):
    dic_main=mainInfoLib.getDic()
    filtro2= { clave: valor for clave, valor in dic_main.armarios_dict.items() if valor.capacidad_cadenas >= cadenas_paralelo}
    armarios_list_sortedPrecio =  sorted(filtro2.values(), key=Armario.getSortKeyPrecio)
    return armarios_list_sortedPrecio[0]

#   cajaCombinatoriaGeneral=caja combinatoria con menor precio para todos los mppts
#   cajasCombinatoria= arreglo de cajas combinatorias por cada mppt
def calculoFinalCajaCombinatorias(cajaCombinatoriaGeneral,cajasCombinatorias):
    seleccionFinal=None
    armarios_list_sortedPrecio =  sorted(cajasCombinatorias, key=Armario.getSortKeyPrecio)
    precioTotal=0
    for armario in armarios_list_sortedPrecio:
        precioTotal +=armario.precio
    if cajaCombinatoriaGeneral !=None:
        if (cajaCombinatoriaGeneral.precio<precioTotal):
            seleccionFinal= cajaCombinatoriaGeneral
        else :
           seleccionFinal= armarios_list_sortedPrecio
    else : 
        seleccionFinal=armarios_list_sortedPrecio
    return seleccionFinal
       
       
"""  Paneles solares:
•	En cada campo se selecciona un modelo de panel y mira l acantidad por mppt, luega
    se mira si algun otro campo tiene en comun modelos de paneles, si lo es se suman las cantidades"""
    

def calculoPanelesSolares(paneles):
    paneles_cantidad= [ (panel,sumaMppts(panel.mttps)) for panel in paneles  ]
    lista=[]
   
    while (len(paneles_cantidad) > 0):
            elemento=paneles_cantidad.pop()#obtengo el primer elemento de la lista para evaluarlo con el resto de la lista
            lista.append(duplicatesPanel(paneles_cantidad,elemento))
            #esta  linea actualiza la lista sin repetidos   
            paneles_cantidad = [panel for panel in paneles_cantidad if panel[0].model_panel_solar_1 != elemento[0].model_panel_solar_1]
    return lista
    
def sumaMppts(mttps):   
    result=0
    for mppt in mttps:
        cadenas_paralelo= mppt.numero_de_cadenas_en_paralelo
        paneles_serie= mppt.numero_de_paneles_en_serie_por_cadena
        result+= cadenas_paralelo*paneles_serie
        
    return result
                
def duplicatesPanel(paneles_cantidad,elemento):
    sum=elemento[1]
    for i in range (0,len(paneles_cantidad)):
        if (elemento[0].model_panel_solar_1==paneles_cantidad[i][0].model_panel_solar_1):
            sum+=paneles_cantidad[i][1]
   
    #print (elemento[0].model_panel_solar_1,sum)
    return (elemento[0].model_panel_solar_1,sum)
    
    
def calculoConductoresFinal(condutoresMppts,conductoresSalidaInversor,conductorCombinacionInversores):
    condutores=aplanarList([condutoresMppts,conductoresSalidaInversor,conductorCombinacionInversores])
    lista=[]
    while (len(condutores) > 0):
            elemento=condutores.pop()#obtengo el primer elemento de la lista para evaluarlo con el resto de la lista
            #lista con los distancias finales sumadas, en caso que comparatn calibre, tipoconductor ymaterial
            lista.append(duplicatesCondutores(condutores,elemento))
            #esta  linea actualiza la lista sin repetidos(elimina los repetidos que ya se hallal sumado en el paso anterior)   
            condutores = [conductor for conductor in condutores if (elemento.tipo_conductor!=conductor.tipo_conductor)and(elemento.material_conductor!=conductor.material_conductor)and(elemento.calibre!=conductor.calibre)]
    conductoresSeleccionados=buscarConductor(lista)
    print conductoresSeleccionados
    return conductoresSeleccionados 
     
def duplicatesCondutores(conductores,elemento):
    sumaDistancia=elemento.distancia
    for i in range (0,len(conductores)):
        if (elemento.tipo_conductor==conductores[i].tipo_conductor)and(elemento.material_conductor==conductores[i].material_conductor)and(elemento.calibre==conductores[i].calibre) :
                sumaDistancia+=conductores[i].distancia
    
    elemento.distancia=sumaDistancia
    return (elemento)
    
#funcion que recibe los conductores con la distancia ya acumulada y retorna la lista con el formato de salida 
def buscarConductor(conductores):
    dic_main=mainInfoLib.getDic()
    resultado=[]
    for conductor in conductores:
        for clave, valor in dic_main.conductores_dict.items():
            if (valor.tipo_conductor==conductor.tipo_conductor
               and valor.material==conductor.material_conductor
               and valor.calibre==conductor.calibre):
                   objResultado=Resultado()
                   objResultado.descripcion=valor.descripcion
                   objResultado.cantidad=conductor.distancia
                   objResultado.unidad="Metros"
                   objResultado.valor_unitario=valor.precio
                   objResultado.valor_total=valor.precio*conductor.distancia
                   resultado.append(objResultado)
    return resultado
    
#_____________________________________Canalización_________________________________    
def calculoCanalizacion(camposFV,combinacionInversores):
    canalizaciones=[]
    bandejasPortacables=[]
    salidaInversoresCanalizacion=[]
    salidaInversoresBandejaPortacable=[]
    canalizacionesResult=[] #arreglo con el retorno e las canalizaciones seleccionadas en cada item
    
    for campoFV in camposFV:
        mpptsCanalizacion=[]
        mpptsFuenteBandeja=[]
        mpptsSalidaBandeja=[]
        for mppt in campoFV.mttps:
            
            if mppt.cableado.input.tipo_alambrado.encode('utf8')==u"Canalización".encode('utf8'):
                canalizaciones.append((mppt.cableado.input,mppt.cableado.input.distancia_del_conductor_mas_largo))
            elif mppt.cableado.input.tipo_alambrado=="Bandeja porta cable":
                mpptsFuenteBandeja.append(mppt)
            
            if mppt.cableado.output.tipo_alambrado.encode('utf8')==u"Canalización".encode('utf8'):
                mpptsCanalizacion.append(mppt)
            elif  mppt.cableado.output.tipo_alambrado=="Bandeja porta cable":
                mpptsSalidaBandeja.append(mppt)
         
        canalizaciones.extend(CanalizacionSalidaFV(mpptsCanalizacion))   
        bandejasPortacables.extend(bandejaPortacableFuente(mpptsFuenteBandeja))
        bandejasPortacables.extend(bandejaPortacableSalida(mpptsSalidaBandeja))
        
        if campoFV.salida_inversor.output.tipo_alambrado.encode('utf8')==u"Canalización".encode('utf8'):
            salidaInversoresCanalizacion.append(campoFV.salida_inversor)
        elif campoFV.salida_inversor.output.tipo_alambrado=="Bandeja porta cable":
            salidaInversoresBandejaPortacable.append(campoFV.salida_inversor)
            
        
    
    canalizaciones.extend(canalizacionSalidaInversor(salidaInversoresCanalizacion))
    bandejasPortacables.extend(bandejaPortacableSalidaInversor(salidaInversoresBandejaPortacable))
    
    
    if combinacionInversores.input.tipo_alambrado.encode('utf8')==u"Canalización".encode('utf8'):
        canalizaciones.extend((combinacionInversores.input, combinacionInversores.input.distancia_del_conductor_mas_largo))
    elif combinacionInversores.input.tipo_alambrado=="Bandeja porta cable":
        longitud=float(combinacionInversores.input.longitud_tramo.replace(',','.'))
        cantidad=  combinacionInversores.input.distancia_del_conductor_mas_largo/longitud
        bandejasPortacables.append((combinacionInversores.input,cantidad))
    
    #buscar similitudes en bandejas portacables y si las hay suar sus cantidades
    combinacionBandejaPortacable=combinarBandejaPortacable(bandejasPortacables)
    #cojer canalizaciones y buscar en la bd Canalizaciones
    canalizacionesResult.extend(buscarCanalilzacion(canalizaciones))
    canalizacionesResult.extend(buscarBandejaPortacable(combinacionBandejaPortacable))
    print canalizacionesResult
    return canalizacionesResult
            
    
def CanalizacionSalidaFV(mppts): 
    lista=[]
    while (len(mppts) > 0):
        elemento=mppts.pop()#obtengo el primer elemento de la lista para evaluarlo con el resto de la lista
        
        lista.append(duplicatesCanalizacionOutput(mppts,elemento))
        #esta  linea actualiza la lista sin repetidos(elimina los repetidos que ya se hallal encontrado en el paso anterior)   
        mppts = [mppt for mppt in mppts if (elemento.cableado.output.tipo_canalizacion!=mppt.cableado.output.tipo_canalizacion and 
            elemento.cableado.output.tamanio_canalizacion!=mppt.cableado.output.tamanio_canalizacion)]
    return lista
            
def duplicatesCanalizacionOutput(mpptsSalida,elemento):
    distanciaMayor=elemento.cableado.output.distancia_del_conductor_mas_largo
    
    for i in range (0,len(mpptsSalida)):
        if (elemento.cableado.output.tipo_canalizacion==mpptsSalida[i].cableado.output.tipo_canalizacion and 
            elemento.cableado.output.tamanio_canalizacion==mpptsSalida[i].cableado.output.tamanio_canalizacion):
                if distanciaMayor< mpptsSalida[i].cableado.output.distancia_del_conductor_mas_largo:
                    distanciaMayor=mpptsSalida[i].cableado.output.distancia_del_conductor_mas_largo
    
    return (elemento.cableado.output,distanciaMayor)
    
def canalizacionSalidaInversor(salidaInversores): 
    lista=[]
    while (len(salidaInversores) > 0):
        elemento=salidaInversores.pop()#obtengo el primer elemento de la lista para evaluarlo con el resto de la lista
        
        lista.append(duplicatesCanalizacionSalidaInversor(salidaInversores,elemento))
        #esta  linea actualiza la lista sin repetidos(elimina los repetidos que ya se hallal encontrado en el paso anterior)   
        salidaInversores = [salidaInversor for salidaInversor in salidaInversores if (elemento.output.tipo_canalizacion!=salidaInversor.output.tipo_canalizacion and 
            elemento.output.tamanio_canalizacion!=salidaInversor.output.tamanio_canalizacion)]
    return lista
    
def duplicatesCanalizacionSalidaInversor(salidaInversores,elemento):
    distancia=elemento.output.distancia_del_conductor_mas_largo
    contador=1
    for i in range (0,len(salidaInversores)):
        if (elemento.output.tipo_canalizacion==salidaInversores[i].output.tipo_canalizacion and 
            elemento.output.tamanio_canalizacion==salidaInversores[i].output.tamanio_canalizacion):
                distancia+=salidaInversores[i].output.distancia_del_conductor_mas_largo
                contador+=1
    return (elemento.output,float(distancia)/contador)
    
def bandejaPortacableFuente(mppts): 
    lista=[]
    while (len(mppts) > 0):
        elemento=mppts.pop()#obtengo el primer elemento de la lista para evaluarlo con el resto de la lista
        lista.append(duplicatesBandejaPortacableInput(mppts,elemento))
        #esta  linea actualiza la lista sin repetidos(elimina los repetidos que ya se hallal encontrado en el paso anterior)   
        mppts = [mppt for mppt in mppts if (elemento.cableado.input.disenio_bandeja!=mppt[i].cableado.input.disenio_bandeja and 
            elemento.cableado.input.material_bandeja!=mppt[i].cableado.input.material_bandeja and 
            elemento.cableado.input.tipo_acabado!=mppt[i].cableado.input.tipo_acabado and 
            elemento.cableado.input.longitud_tramo!=mppt[i].cableado.input.longitud_tramo and 
            elemento.cableado.input.ancho_mm!=mppt[i].cableado.input.ancho_mm and 
            elemento.cableado.input.alto_mm!=mppt[i].cableado.input.alto_mm and 
            elemento.cableado.input.tipo_carga!=mppt[i].cableado.input.tipo_carga)]
    return lista
    
def duplicatesBandejaPortacableInput(mpptsEntrada,elemento):
    distanciaMayor=elemento.cableado.input.distancia_del_conductor_mas_largo
    
    for i in range (0,len(mpptsEntrada)):
        if (elemento.cableado.input.disenio_bandeja==mpptsEntrada[i].cableado.input.disenio_bandeja and 
            elemento.cableado.input.material_bandeja==mpptsEntrada[i].cableado.input.material_bandeja and 
            elemento.cableado.input.tipo_acabado==mpptsEntrada[i].cableado.input.tipo_acabado and 
            elemento.cableado.input.longitud_tramo==mpptsEntrada[i].cableado.input.longitud_tramo and 
            elemento.cableado.input.ancho_mm==mpptsEntrada[i].cableado.input.ancho_mm and 
            elemento.cableado.input.alto_mm==mpptsEntrada[i].cableado.input.alto_mm and 
            elemento.cableado.input.tipo_carga==mpptsEntrada[i].cableado.input.tipo_carga):
                if distanciaMayor< mpptsEntrada[i].cableado.input.distancia_del_conductor_mas_largo:
                    distanciaMayor=mpptsEntrada[i].cableado.input.distancia_del_conductor_mas_largo
    longitud=float(elemento.cableado.input.longitud_tramo.replace(',','.'))
    return (elemento.cableado.input,distanciaMayor/longitud)

def bandejaPortacableSalida(mppts): 
    lista=[]
    while (len(mppts) > 0):
        elemento=mppts.pop()#obtengo el primer elemento de la lista para evaluarlo con el resto de la lista
        lista.append(duplicatesBandejaPortacableOutput(mppts,elemento))
        #esta  linea actualiza la lista sin repetidos(elimina los repetidos que ya se hallal encontrado en el paso anterior)   
        mppts = [mppt for mppt in mppts if (elemento.cableado.input.disenio_bandeja!=mppt[i].cableado.input.disenio_bandeja and 
            elemento.cableado.input.material_bandeja!=mppt[i].cableado.input.material_bandeja and 
            elemento.cableado.input.tipo_acabado!=mppt[i].cableado.input.tipo_acabado and 
            elemento.cableado.input.longitud_tramo!=mppt[i].cableado.input.longitud_tramo and 
            elemento.cableado.input.ancho_mm!=mppt[i].cableado.input.ancho_mm and 
            elemento.cableado.input.alto_mm!=mppt[i].cableado.input.alto_mm and 
            elemento.cableado.input.tipo_carga!=mppt[i].cableado.input.tipo_carga)]
    return lista
    
def duplicatesBandejaPortacableOutput(mpptsEntrada,elemento):
    distanciaMayor=elemento.cableado.output.distancia_del_conductor_mas_largo
    
    for i in range (0,len(mpptsEntrada)):
        if (elemento.cableado.output.disenio_bandeja==mpptsEntrada[i].cableado.output.disenio_bandeja and 
            elemento.cableado.output.material_bandeja==mpptsEntrada[i].cableado.output.material_bandeja and 
            elemento.cableado.output.tipo_acabado==mpptsEntrada[i].cableado.output.tipo_acabado and 
            elemento.cableado.output.longitud_tramo==mpptsEntrada[i].cableado.output.longitud_tramo and 
            elemento.cableado.output.ancho_mm==mpptsEntrada[i].cableado.output.ancho_mm and 
            elemento.cableado.output.alto_mm==mpptsEntrada[i].cableado.output.alto_mm and 
            elemento.cableado.output.tipo_carga==mpptsEntrada[i].cableado.output.tipo_carga):
                if distanciaMayor< mpptsEntrada[i].cableado.output.distancia_del_conductor_mas_largo:
                    distanciaMayor=mpptsEntrada[i].cableado.output.distancia_del_conductor_mas_largo
    longitud=float(elemento.cableado.output.longitud_tramo.replace(',','.'))
    return (elemento.cableado.output,distanciaMayor/longitud)
    
def bandejaPortacableSalidaInversor(salidaInversores): 
    lista=[]
    while (len(salidaInversores) > 0):
        elemento=salidaInversores.pop()#obtengo el primer elemento de la lista para evaluarlo con el resto de la lista
        
        lista.append(duplicatesBandejaPortacableSalidaInversor(salidaInversores,elemento))
        #esta  linea actualiza la lista sin repetidos(elimina los repetidos que ya se hallal encontrado en el paso anterior)   
        salidaInversores = [salidaInversor for salidaInversor in salidaInversores if (elemento.output.disenio_bandeja!=salidaInversor[i].output.disenio_bandeja and 
            elemento.output.material_bandeja!=salidaInversor[i].output.material_bandeja and 
            elemento.output.tipo_acabado!=salidaInversor[i].output.tipo_acabado and 
            elemento.output.longitud_tramo!=salidaInversor[i].output.longitud_tramo and 
            elemento.output.ancho_mm!=salidaInversor[i].output.ancho_mm and 
            elemento.output.alto_mm!=salidaInversor[i].output.alto_mm and 
            elemento.output.tipo_carga!=salidaInversor[i].output.tipo_carga)]
    return lista
    
def duplicatesBandejaPortacableSalidaInversor(salidaInversores,elemento):
    distancia=elemento.output.distancia_del_conductor_mas_largo
    contador=1
    for i in range (0,len(salidaInversores)):
       if (elemento.output.disenio_bandeja==salidaInversores[i].output.disenio_bandeja and 
            elemento.output.material_bandeja==salidaInversores[i].output.material_bandeja and 
            elemento.output.tipo_acabado==salidaInversores[i].output.tipo_acabado and 
            elemento.output.longitud_tramo==salidaInversores[i].output.longitud_tramo and 
            elemento.output.ancho_mm==salidaInversores[i].output.ancho_mm and 
            elemento.output.alto_mm==salidaInversores[i].output.alto_mm and 
            elemento.output.tipo_carga==salidaInversores[i].output.tipo_carga):
                distancia+=salidaInversores[i].output.distancia_del_conductor_mas_largo
                contador+=1
    promedio=float(distancia)/contador
    longitud=float(elemento.output.longitud_tramo.replace(',','.'))
    cantidad=promedio/longitud
    return (elemento.output,promedio/cantidad)
    
def combinarBandejaPortacable(bandejasPortacables): 
    lista=[]
    l=[]
    while (len(bandejasPortacables) > 0):
        
        elemento=bandejasPortacables.pop()#obtengo el primer elemento de la lista para evaluarlo con el resto de la lista
        lista.append(duplicatesBandejaPortacable(bandejasPortacables,elemento))
        #esta  linea actualiza la lista sin repetidos(elimina los repetidos que ya se hallal encontrado en el paso anterior)   
        
        bandejasPortacables=[bandejaPortacable  for bandejaPortacable in bandejasPortacables 
                            if( elemento[0].disenio_bandeja!=bandejaPortacable[0].disenio_bandeja or 
                                elemento[0].material_bandeja!=bandejaPortacable[0].material_bandeja or 
                                elemento[0].tipo_acabado!=bandejaPortacable[0].tipo_acabado or 
                                elemento[0].longitud_tramo!=bandejaPortacable[0].longitud_tramo or 
                                elemento[0].ancho_mm!=bandejaPortacable[0].ancho_mm or 
                                elemento[0].alto_mm!=bandejaPortacable[0].alto_mm or 
                                elemento[0].tipo_carga!=bandejaPortacable[0].tipo_carga)]    
             
    return lista
    
def duplicatesBandejaPortacable(bandejasPortacables,elemento):
    sumaCantidad=elemento[1]
    for i in range (0,len(bandejasPortacables)):
        if (elemento[0].disenio_bandeja==bandejasPortacables[i][0].disenio_bandeja and 
            elemento[0].material_bandeja==bandejasPortacables[i][0].material_bandeja and 
            elemento[0].tipo_acabado==bandejasPortacables[i][0].tipo_acabado and 
            elemento[0].longitud_tramo==bandejasPortacables[i][0].longitud_tramo and 
            elemento[0].ancho_mm==bandejasPortacables[i][0].ancho_mm and 
            elemento[0].alto_mm==bandejasPortacables[i][0].alto_mm and 
            elemento[0].tipo_carga==bandejasPortacables[i][0].tipo_carga):
                sumaCantidad+=bandejasPortacables[i][1]
    return (elemento[0],sumaCantidad)

  
def buscarCanalilzacion(canalizaciones):
    dic_main=mainInfoLib.getDic()
    resultado=[]
    for canalizacion in canalizaciones:
        for clave, valor in dic_main.canalizaciones_dict.items():
            tamanioConvert=unidecode( canalizacion[0].tamanio_canalizacion).replace(" ","")
            
            if (valor.tipo_canalizacion==canalizacion[0].tipo_canalizacion and 
                valor.tamanio.replace(" ","")==tamanioConvert):      
                   objResultado=Resultado(descripcion=valor.descripcion,cantidad=canalizacion[1],
                                          unidad="Metros",valor_unitario=valor.precio,valor_total=valor.precio*canalizacion[1])
                  
                   resultado.append(objResultado)
    return resultado
    

def buscarBandejaPortacable(bandejasPortacables):
    dic_main=mainInfoLib.getDic()
    resultado=[]
    for bandejaPortacable in bandejasPortacables:
        for clave, valor in dic_main.bandejasPortacables_dict.items():
            if (valor.disenio==bandejaPortacable[0].disenio_bandeja and 
                valor.material==bandejaPortacable[0].material_bandeja and 
                valor.acabado==bandejaPortacable[0].tipo_acabado and 
                float(valor.longitud)==float(bandejaPortacable[0].longitud_tramo.replace(",",".")) and 
                float(valor.ancho)==float(bandejaPortacable[0].ancho_mm) and 
                float(valor.alto)==float(bandejaPortacable[0].alto_mm) and 
                valor.tipo_carga==bandejaPortacable[0].tipo_carga):
                    objResultado=Resultado(descripcion=valor.descripcion,cantidad=bandejaPortacable[1],
                                          unidad="Metros",valor_unitario=valor.precio,valor_total=valor.precio*bandejaPortacable[1])
                    #print objResultado.descripcion
                    resultado.append(objResultado)
                   
    return resultado