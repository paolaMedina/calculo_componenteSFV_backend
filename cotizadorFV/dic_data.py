class Dic_data():
    def __init__(self,interruptoresManuales_dict ={},interruptoresAuto_dict={},panelesSolares_dict={},dpsAC_dict={},
                dpsDC_dict={},fusible_dict={}, inversores_dict={},canalizaciones_dict={},
                bandejasPortacables_dict={},conductores_dict={},accesorios_dict={},armarios_dict={}):
        
        self.interruptoresManuales_dict=interruptoresManuales_dict
        self.interruptoresAuto_dict=interruptoresAuto_dict
        self.panelesSolares_dict=panelesSolares_dict
        self.dpsAC_dict=dpsAC_dict
        self.dpsDC_dict=dpsDC_dict
        self.fusible_dict=fusible_dict
        self.inversores_dict=inversores_dict
        self.canalizaciones_dict=canalizaciones_dict
        self.bandejasPortacables_dict=bandejasPortacables_dict
        self.conductores_dict=conductores_dict
        self.accesorios_dict=accesorios_dict
        self.armarios_dict=armarios_dict
        
        
    def setInterruptoresManuales_dict(self,interruptoresManuales_dict):
        self.interruptoresManuales_dict=interruptoresManuales_dict
    def setInterruptoresAuto_dict(self,interruptoresAuto_dict):
        self.interruptoresAuto_dict=interruptoresAuto_dict
    def setPanelesSolares_dict(self,panelesSolares_dict):
        self.panelesSolares_dict=panelesSolares_dict
    def setDpsAC_dict(self,dpsAC_dict):
        self.dpsAC_dict=dpsAC_dict
    def setDpsDC_dict(self,dpsDC_dict):
        self.dpsDC_dict=dpsDC_dict
    def setFusible_dict(self,fusible_dict):
        self.fusible_dict=fusible_dict
    def setInversores_dict(self,inversores_dict):
        self.inversores_dict=inversores_dict
    def setCanalizaciones_dict(self,canalizaciones_dict):
        self.canalizaciones_dict=canalizaciones_dict
    def setBandejasPortacables_dict(self,bandejasPortacables_dict):
        self.bandejasPortacables_dict=bandejasPortacables_dict
    def setConductores_dict(self,conductores_dict):
        self.conductores_dict=conductores_dict
    def setAccesorios_dict(self,accesorios_dict):
        self.accesorios_dict=accesorios_dict
    def setArmarios_dict(self,armarios_dict):
        self.armarios_dict=armarios_dict
        
dic_inicial=Dic_data()
        
    
     