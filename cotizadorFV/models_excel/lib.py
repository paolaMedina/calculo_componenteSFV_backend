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

def importarDpsAC():
    dpssAC = importcsv(DpsAC, 'archivo/DPS_AC.csv')
    inicial.setDpsAC(dpssAC)
def importarDpsDC():
    dpssDC = importcsv(DpsDC, 'archivo/DPS_AC.csv')
    inicial.setDpsDC(dpssDC)
def importarCsvs():
    importarInterruptoresManuales()
    importarPanelesSolares()