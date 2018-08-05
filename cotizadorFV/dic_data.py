class Dic_data():
    def __init__(self,interruptoresManuales_dict ={},panelesSolares_dict={},dpsAC_dict={},dpsDC_dict={},fusible_dict={}, inversores_dict={}):
        
        self.interruptoresManuales_dict=interruptoresManuales_dict
        self.panelesSolares_dict=panelesSolares_dict
        self.dpsAC_dict=dpsAC_dict
        self.dpsDC_dict=dpsDC_dict
        self.fusible_dict=fusible_dict
        self.inversores_dict=inversores_dict
        
        
    def setInterruptoresManuales_dict(self,interruptoresManuales_dict):
        self.interruptoresManuales_dict=interruptoresManuales_dict
        
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
        
dic_inicial=Dic_data()
        
    
     