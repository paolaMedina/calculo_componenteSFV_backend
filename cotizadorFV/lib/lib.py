from cotizadorFV.modelsCSV import *
from cotizadorFV.main_info import inicial
from cotizadorFV.dic_data import dic_inicial

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
    interruptores_manuales = importcsv(InterruptorManual, 'media/archivosCSV/interruptores_manuales.csv')
    inicial.setInterruptoresManuales(interruptores_manuales)

def importarPanelesSolares():
    panelesSolares = importcsv(PanelSolar, 'media/archivosCSV/panelesSolares.csv')
    inicial.setPanelesSolares(panelesSolares)
def importarMicroInversores():
    microInversores = importcsv(MicroInversor, 'media/archivosCSV/microinversor.csv')
    inicial.setMicroInversores(microInversores)
    print(inicial.microInversores[0])
def importarDpsAC():
    dpssAC = importcsv(DpsAC, 'media/archivosCSV/DPS_AC.csv')
    inicial.setDpsAC(dpssAC)
    
    
def importarDpsDC():
    dpssDC = importcsv(DpsDC, 'media/archivosCSV/DPS_DC.csv')
    inicial.setDpsDC(dpssDC)
    
def importarFusible():
    fusibles = importcsv(Fusible, 'media/archivosCSV/fusibles.csv')
    inicial.setFusibles(fusibles)

def importarInterruptoresAuto():
    interruptoresAuto = importcsv(InteAuto, 'media/archivosCSV/interruptores_automaticos.csv')
    inicial.setInterruptoresAutomaticos(interruptoresAuto)
    
def importarInversores():
    inversores = importcsv(Inversor, 'media/archivosCSV/inversor.csv')
    inicial.setInversores(inversores)
    
    
def importarCsvs():
    importarInterruptoresManuales()
    importarPanelesSolares()
    importarDpsAC()
    importarDpsDC()
    importarFusible()
    importarInterruptoresAuto()
    importarMicroInversores()
    importarInversores()
    makeDic()
    
    
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
    print (dpsAC_dict["DS250E-120"].precio)
    
    
def getDic():
    return dic_inicial
