from . import constants

correcion_tem_amb= constants.correcion_tem_amb
factorAjusteConductores=constants.factorAjusteConductores
calibre=constants.calibre
area_calibre=constants.area_calibre


def calculo_caidaTension(i,l,s,v):
    print "i "+ str(i)
    print "l " +str(l)
    print "s "+ str(s)
    print "v " +str(v)
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
    
    
#_________________________________________________CIRCUITO DE FUENTE FV_____________________________________________
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

def corrienteNominalEntrada(tem_amb,max_conductores,isc_panel):
    kt=correcionTemp(tem_amb)
    kr=factorLlenado(max_conductores)
    
    return isc_panel*1.56/(kt*kr) 
    

def posicionCalibreFuente(tem_amb,max_conductores,isc_panel):
    posicion=0
    corr_nominal=corrienteNominalEntrada(tem_amb,max_conductores,isc_panel)
    for i in range(len(calibre)):
        if (corr_nominal<=calibre[i][1]):
            posicion=i
            break
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
    
    
def posicionCalibreSalida(tem_amb,max_conductores,isc_panel,cadenas_paralelo):
    posicion=0
    corr_nominal=corrienteNominalSalida(tem_amb,max_conductores,isc_panel,cadenas_paralelo)
    for i in range(len(calibre)):
        if (corr_nominal<=calibre[i][1]):
            posicion=i
            break
    return posicion
    

def caidaTensionSalida(posicionCalibre,distanciaConductor,corrienteMPP,tension_Mpp):
    calibreSeleccionado=calibre[posicionCalibre][0]
    conductor_seleccionado=seleccionarConductor(calibreSeleccionado)
    caida_tension=calculo_caidaTension(corrienteMPP,distanciaConductor,conductor_seleccionado,tension_Mpp)
    return caida_tension
    
"""
def caidaTensionSalidaInicial(tem_amb,max_conductores,isc_panel,cadenas_paralelo,distanciaConductor,corrienteMPP,tension_Mpp):
    posicionCalibre=posicionCalibreSalida(tem_amb,max_conductores,isc_panel,cadenas_paralelo)
    calibre=calibre[posicionCalibre][0]
   
    caidaTensionSalida(calibre,distanciaConductor,corrienteMPP,tension_Mpp)
"""
    
#__________________________________________________________   
    
#Suma de tensiones entrada-salida
def seleccionCalibre(tem_amb,max_conductoresFuente,max_conductoresSalida,isc_panel,impp_panel,cadenas_paralelo,distanciaConductorFuente,
                    distanciaConductorSalida,corrienteMPP,tension_Mpp,tensionFuenteDiseno,tensionSalidaDiseno):
                         
    #caida de tension fuente inicial                    
    posCalibreFuente=posicionCalibreFuente(tem_amb,max_conductoresFuente,isc_panel)
    caidaTensionF=caidaTensionFuente(posCalibreFuente,tension_Mpp,impp_panel,distanciaConductorFuente)
 
    
    #caida de tension salida inicial                    
    posCalibreSalida=posicionCalibreSalida(tem_amb,max_conductoresSalida,isc_panel,cadenas_paralelo)
    caidaTensionS=caidaTensionSalida(posCalibreSalida,distanciaConductorSalida,corrienteMPP,tension_Mpp)
    
    
    
    suma_caida_tension_diseno=tensionFuenteDiseno+tensionSalidaDiseno
    for i in range(len(calibre)):
        suma_caida_tension=caidaTensionF+caidaTensionS
        print ("estoy en el for")
        
        if (suma_caida_tension>suma_caida_tension_diseno):
            if (caidaTensionF>caidaTensionS):
                posCalibreFuente +=1
                print posCalibreFuente
                caidaTensionF=caidaTensionFuente(posCalibreFuente,tension_Mpp,impp_panel,distanciaConductorFuente)
            else:
                posCalibreSalida +=1
                caidaTensionS=caidaTensionSalida(posicionCalibreSalida,distanciaConductorSalida,corrienteMPP,tension_Mpp)
        else: 
            print "else"
            break
                
    
    print ("fuente ")
    print (format(caidaTensionF, '.2f'))
    print ("salida ")
    print (format(caidaTensionS, '.2f'))
    