from . import constants

correcion_tem_amb= constants.correcion_tem_amb
factorAjusteConductores=constants.factorAjusteConductores
calibre=constants.calibre
area_calibre=constants.area_calibre
calibreConductor=constants.calibreConductor
calibreAire=constants.calibreAire


    
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
        print "soy aire"
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
    kr=factorLlenado(max_conductores)
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
    

    
#__________________________________________________________   
    
#seleccionar el calibre que cumple con la tension ingresada por el usuario
def seleccionCalibre(tem_amb,max_conductoresFuente,max_conductoresSalida,isc_panel,impp_panel,cadenas_paralelo,distanciaConductorFuente,
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
                print posCalibreFuente
                caidaTensionF=caidaTensionFuente(posCalibreFuente,tension_Mpp,impp_panel,distanciaConductorFuente)
            else:
                posCalibreSalida +=1
                caidaTensionS=caidaTensionSalida(posicionCalibreSalida,distanciaConductorSalida,corrienteMPP,tension_Mpp)
        else: 
            break
                
    
    print ("calibre fuente ")
    print (calibre[posCalibreFuente][0])
    print ("calibre salida ")
    print (calibre[posCalibreSalida][0])
    
    #falta retornar array
    
    
#___________________________________________Salida Inversor___________________________________________________---


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
    

def caidaTensionInversor(posicionCalibre,isal,tem_amb,max_conductores,isc_panel,l,v):
    cos=1
    r=44
    calibreSeleccionado=calibre[posicionCalibre][0]
    s=seleccionarConductor(calibreSeleccionado)#conductor_seleccionado
    i=corrienteNominalInversor(isal,tem_amb,max_conductores,isc_panel)#corriente nominal salida
    caida_tension= (i*l*cos)/(r*s)*100/v
    
    
    return caida_tension
    
#def seleccionCalibreInversor(isal,tem_amb,max_conductores,isc_panel,l,v,caidaTensionUsuario)


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
def calibreconductorAC(isal,sumIsal,tem_amb,max_conductores,isc_panel): 
    corrienteNominalEntrada=corrienteNominalInversor(isal,tem_amb,max_conductores,isc_panel)
    corrienteNominalSalida=corrienteNominalInversor(sumIsal,tem_amb,max_conductores,isc_panel)
    
    calibreEntrada=buscarCalibreCondutor(corrienteNominalEntrada)
    calibreSalida=buscarCalibreCondutor(corrienteNominalSalida)
    
    ##falta retornar array
    