class MainInfo():
    def __init__(self, interruptoresManuales=[], panelesSolares=[], dpssAC=[], dpssDC=[],
                fusibles=[], interruptoresAutomaticos=[],inversores=[], microInversores=[]):
        """Init main info
        
        Keyword Arguments:
            interruptoresManuales {list of InterruptoresManuales} -- [description] (default: {[]})
            panelesSolares {list of PanelesSolares} -- [description] (default: {[]})
            dpssAC {list of DpsAC} -- [description] (default: {[]})
            dpssDC {list of DpsDC} -- [description] (default: {[]})
            microInversores {list of MicroInversores} -- [description] (default: {[]})
        """
        self.interruptoresManuales = interruptoresManuales
        self.panelesSolares = panelesSolares
        self.dpssAC = dpssAC
        self.dpssDC = dpssDC
        self.fusibles = fusibles
        self.interruptoresAutomaticos = interruptoresAutomaticos
        self.inversores = inversores
        self.microInversores = microInversores
        
        
        
        
        
    def setInterruptoresManuales(self, interruptoresManuales):
        self.interruptoresManuales = interruptoresManuales
    def setPanelesSolares(self, panelesSolares):
        self.panelesSolares = panelesSolares
    def setDpsAC(self, dpssAC):
        self.dpssAC = dpssAC
    def setDpsDC(self, dpssDC):
        self.dpssDC = dpssDC
    def setFusibles(self, fusibles):
        self.fusibles = fusibles
    def setInterruptoresAutomaticos(self, interruptoresAutomaticos):
        self.interruptoresAutomaticos = interruptoresAutomaticos
    def setInversores(self, inversores):
        self.inversores = inversores
    def setMicroInversores(self, microInversores):
        self.microInversores = microInversores
        
inicial=MainInfo()