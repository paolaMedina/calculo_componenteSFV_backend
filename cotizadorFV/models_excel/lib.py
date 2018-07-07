from cotizadorFV.modelsCVS import *
from cotizadorFV.main_info import inicial

def importcsv(modelo_csv, nombre_archivo):
    """Funcion generica para cargar archivos csv usando modelos de `django-adaptor` 
    Los resultados se retornan en una lista
    
    Arguments:
        modelo_csv {[CsvModel]} -- [description]
        lista_objetivo {[list]} -- [description]
        nombre_archivo {[string]} -- [description]
    """
    data = open(nombre_archivo).readlines()
    if( hasattr(modelo_csv, 'Meta') and hasattr(modelo_csv.Meta, 'has_header') and modelo_csv.Meta.has_header ):
        data = data[1:]
    my_csv_list = modelo_csv.import_data(data = data)
    return [my_csv_list[i] for i in range(0, len(my_csv_list))]
    

def importarInterruptoresManuales():
    interruptores_manuales = importcsv(InterruptorManual, 'archivo/interruptores_manuales_DC.csv')
    inicial.setInterruptoresManuales(interruptores_manuales)

def importarPanelesSolares():
    panelesSolares = importcsv(PanelSolar, 'archivo/panelesSolares.csv')
    inicial.setPanelesSolares(panelesSolares)
def importarMicroInversores():
    microInversores = importcsv(MicroInversor, 'archivo/microinversor.csv')
    inicial.setMicroInversores(microInversores)
    print(inicial.microInversores[0])
def importarDpsAC():
    dpssAC = importcsv(DpsAC, 'archivo/DPS_AC.csv')
    inicial.setDpsAC(dpssAC)
    
    
def importarDpsDC():
    dpssDC = importcsv(DpsDC, 'archivo/DPS_DC.csv')
    inicial.setDpsDC(dpssDC)
    
def importarFusible():
    fusibles = importcsv(Fusible, 'archivo/fusibles.csv')
    inicial.setFusibles(fusibles)

def importarInterruptoresAuto():
    interruptoresAuto = importcsv(InteAuto, 'archivo/interruptores_automaticos.csv')
    inicial.setInterruptoresAutomaticos(interruptoresAuto)
    
def importarInversores():
    inversores = importcsv(Inversor, 'archivo/inversor.csv')
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
def getData():
    return inicial

