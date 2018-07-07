from cotizadorFV.modelsCVS import InterruptorManual, PanelSolar
from cotizadorFV.main_info import inicial

def importcsv(modelo_csv, nombre_archivo):
    """Funcion generica para cargar archivos csv usando modelos de `django-adaptor` 
    Los resultados se retornan en una lista
    
    Arguments:
        modelo_csv {[CsvModel]} -- [description]
        lista_objetivo {[list]} -- [description]
        nombre_archivo {[string]} -- [description]
    """
    my_csv_list = modelo_csv.import_data(data = open(nombre_archivo))
    return [my_csv_list[i] for i in range(1, len(my_csv_list))]
    

def importarInterruptoresManuales():
    interruptores_manuales = importcsv(InterruptorManual, 'archivo/interruptores_manuales_DC.csv')
    inicial.setInterruptoresManuales(interruptores_manuales)
    print(interruptores_manuales)

def importarPanelesSolares():
    panelesSolares = importcsv(PanelSolar, 'archivo/panelesSolares.csv')
    inicial.setPanelesSolares(panelesSolares)

def importarCsvs():
    importarInterruptoresManuales()
    importarPanelesSolares()