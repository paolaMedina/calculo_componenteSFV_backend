# -*- coding: utf-8 -*-

from . import constants
from cotizadorFV.modelsCSV import *
from cotizadorFV.lib import lib as mainInfoLib
import math

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
    

    
    
#Seleccionar el calibre que cumple con la tension ingresada por el usuario
def CalculoConductores(tem_amb,max_conductoresFuente,max_conductoresSalida,isc_panel,impp_panel,cadenas_paralelo,distanciaConductorFuente,
                    distanciaConductorSalida,corrienteMPP,tension_Mpp,tensionFuenteDiseno,tensionSalidaDiseno,tipo_alambradoEntrada,tipo_alambradoSalida):
                        
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
                
    
    #print ("calibre fuente ")
    #print (calibre[posCalibreFuente][0])
    #print ("calibre salida ")
    #print (calibre[posCalibreSalida][0])
    calibresES=[calibre[posCalibreFuente][0],calibre[posCalibreSalida][0]] 
    return calibresES
    
    #falta retornar array
    
    
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

#funcion que entrega el  calibre salida para el inversor  y  tambien se usa para circuito de invesor combinadoo (isal=suma de los isal de los inversore)
def CalculoConductorInversor(tipo_servicio,isal,tem_amb,max_conductoresSalida,isc_panel,distanciaConductorSalida,tensionServicio,caidaTensionUsuarioSalida):
    conductoresInversor=None

    posicionCalibreSalida=posicionCalibreInversor(isal,tem_amb,max_conductoresSalida,isc_panel)
    caidaTensionSalida=caidaTensionInversor(tipo_servicio,posicionCalibreSalida,isal,tem_amb,max_conductoresSalida,isc_panel,distanciaConductorSalida,tensionServicio)
    
    for i in range(len(calibre)):
        if (caidaTensionSalida>caidaTensionUsuarioSalida):
                posicionCalibreSalida +=1
                caidaTensionSalida=caidaTensionInversor(tipo_servicio,posicionCalibreSalida,isal,tem_amb,max_conductoresSalida,isc_panel,distanciaConductorSalida,tensionServicio)
        else: 
            break
    conductoresInversor=calibre[posicionCalibreSalida][0]
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
    