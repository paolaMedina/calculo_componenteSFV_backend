class MainInfo():
    def __init__(self, interruptores_manuales=[], paneles_solares=[]):
        """[summary]
        
        Keyword Arguments:
            interruptores_manuales {list of InterruptoresManuales} -- [description] (default: {[]})
            paneles_solares {list of PanelesSolares} -- [description] (default: {[]})
        """
        self.interruptores_manuales = interruptores_manuales
        self.paneles_solares = paneles_solares
    def setInterruptoresManuales(self, interruptores_manuales):
        self.interruptores_manuales = interruptores_manuales
    def setPanelesSolares(self, paneles_solares):
        self.paneles_solares = paneles_solares


inicial=MainInfo()