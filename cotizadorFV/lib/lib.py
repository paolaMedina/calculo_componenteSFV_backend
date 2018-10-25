# -*- coding: utf-8 -*-
from cotizadorFV.modelsCSV import *
from cotizadorFV.main_info import inicial
from cotizadorFV.dic_data import dic_inicial
from django.conf import settings

def importcsv(modelo_csv, nombre_archivo):
    """Funcion generica para cargar media/archivosCSVs csv usando modelos de `django-adaptor` 
    Los resultados se retornan en una lista
    
    Arguments:
        modelo_csv {[CsvModel]} -- [description]
        lista_objetivo {[list]} -- [description]
        nombre_media/archivosCSV {[string]} -- [description]
    """
    data = open(nombre_archivo).readlines()
    if( hasattr(modelo_csv, 'Meta') and hasattr(modelo_csv.Meta, 'has_header') and modelo_csv.Meta.has_header ):
        data = data[1:]
    my_csv_list = modelo_csv.import_data(data = data)
    return [my_csv_list[i] for i in range(0, len(my_csv_list))]
    

def importarInterruptoresManuales():
    interruptores_manuales = importcsv(InterruptorManual, (settings.BASE_DIR)+'/media/archivosCSV/interruptores_manuales.csv')
    inicial.setInterruptoresManuales(interruptores_manuales)

def importarPanelesSolares():
    panelesSolares = importcsv(PanelSolar, (settings.BASE_DIR)+'/media/archivosCSV/panelesSolares.csv')
    inicial.setPanelesSolares(panelesSolares)
def importarMicroInversores():
    microInversores = importcsv(MicroInversor, (settings.BASE_DIR)+'/media/archivosCSV/microinversor.csv')
    inicial.setMicroInversores(microInversores)
    
def importarDpsAC():
    dpssAC = importcsv(DpsAC, (settings.BASE_DIR)+'/media/archivosCSV/DPS_AC.csv')
    inicial.setDpsAC(dpssAC)
    
    
def importarDpsDC():
    dpssDC = importcsv(DpsDC, (settings.BASE_DIR)+'/media/archivosCSV/DPS_DC.csv')
    inicial.setDpsDC(dpssDC)
    
def importarFusible():
    fusibles = importcsv(Fusible, (settings.BASE_DIR)+'/media/archivosCSV/fusibles.csv')
    inicial.setFusibles(fusibles)

def importarInterruptoresAuto():
    interruptoresAuto = importcsv(InteAuto, (settings.BASE_DIR)+'/media/archivosCSV/interruptores_automaticos.csv')
    inicial.setInterruptoresAutomaticos(interruptoresAuto)
    
def importarInversores():
    inversores = importcsv(Inversor, (settings.BASE_DIR)+'/media/archivosCSV/inversor.csv')
    inicial.setInversores(inversores)

def importarCanalizaciones():
    canalizaciones = importcsv(Canalizacion, (settings.BASE_DIR)+'/media/archivosCSV/Canalizacion.csv')
    inicial.setCanalizaciones(canalizaciones)

def importarBandejasPortacables():
    bandejasPortacables = importcsv(BandejaPortacable, (settings.BASE_DIR)+'/media/archivosCSV/Bandeja_Portacable.csv')
    inicial.setBandejasPortacables(bandejasPortacables)
    
def importarConductores():
    conductores = importcsv(Conductor, (settings.BASE_DIR)+'/media/archivosCSV/Conductores.csv')
    inicial.setConductores(conductores)
    
def importarAccesorios():
    accesorios = importcsv(Accesorio, (settings.BASE_DIR)+'/media/archivosCSV/Accesorios.csv')
    inicial.setAccesorios(accesorios)
    
def importarArmarios():
    armarios = importcsv(Armario, (settings.BASE_DIR)+'/media/archivosCSV/Armarios.csv')
    inicial.setArmarios(armarios)
     

def importarCsvs():
    importarInterruptoresManuales()
    importarPanelesSolares()
    importarDpsAC()
    importarDpsDC()
    importarFusible()
    importarInterruptoresAuto()
    importarMicroInversores()
    importarInversores()
    importarCanalizaciones()
    importarBandejasPortacables()
    importarConductores()
    importarAccesorios()
    importarArmarios()
    makeDic()#diccionario con la bd
    
    
def getData():
    return inicial



def makeDic():
    #interurptores manuales
    interruptoresManuales_dict = {x.referencia: x for x in inicial.interruptoresManuales}
    dic_inicial.setInterruptoresManuales_dict(interruptoresManuales_dict)
    #interruptorres automaticos
    interruptoresAuto_dict = {x.referencia: x for x in inicial.interruptoresAutomaticos}
    dic_inicial.setInterruptoresAuto_dict(interruptoresAuto_dict)
    #paneles solares
    panelesSolares_dict= {x.descripcion: x for x in inicial.panelesSolares}
    dic_inicial.setPanelesSolares_dict(panelesSolares_dict)
    #dps AC
    dpsAC_dict= {x.referencia: x for x in inicial.dpssAC}
    dic_inicial.setDpsAC_dict(dpsAC_dict)
    #dps DC
    dpsDC_dict= {x.descripcion: x for x in inicial.dpssDC}
    dic_inicial.setDpsDC_dict(dpsDC_dict)
    #fusibles
    fusible_dict= {x.referencia: x for x in inicial.fusibles}
    dic_inicial.setFusible_dict(fusible_dict)
    #inversores
    inversor_dict= {x.descripcion: x for x in inicial.inversores}
    dic_inicial.setInversores_dict(inversor_dict)
    #Canalizacion
    canalizacion_dict= {x.descripcion: x for x in inicial.canalizaciones}
    dic_inicial.setCanalizaciones_dict(canalizacion_dict)
    #bandejaPortacable
    bandejaPortacable_dict= {x.descripcion: x for x in inicial.bandejasPortacables}
    dic_inicial.setBandejasPortacables_dict(bandejaPortacable_dict)
    #conductores
    conductores_dict= {x.descripcion: x for x in inicial.conductores}
    dic_inicial.setConductores_dict(conductores_dict)
    #Accesorios
    accesorios_dict= {x.descripcion: x for x in inicial.accesorios}
    dic_inicial.setAccesorios_dict(accesorios_dict)
    #Armarios
    armarios_dict= {x.descripcion: x for x in inicial.armarios}
    dic_inicial.setArmarios_dict(armarios_dict)
    
    
def getDic():
    return dic_inicial
