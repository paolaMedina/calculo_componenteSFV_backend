class MicroInversor:
	def __init__(self, descripcion , modelo , fabricante , pot_fv_in_min , pot_fv_in_max , vin_min , 
		vin_max , vop_min , vop_max , vreg_min , vreg_max , isc_max , psal_max , 
		psal_nom , tipo_conex , v_nom1 , v_nom2 , i_nom1 , i_nom2 ):
        self.descripcion = descripcion
        self.modelo = modelo
        self.fabricante = fabricante
        self.pot_fv_in_min = pot_fv_in_min
        self.pot_fv_in_max = pot_fv_in_max
        self.vin_min = vin_min
        self.vin_max = vin_max
        self.vop_min = vop_min
        self.vop_max = vop_max
        self.vreg_min = vreg_min
        self.vreg_max = vreg_max
        self.isc_max = isc_max
        self.psal_max = psal_max
        self.psal_nom = psal_nom
        self.tipo_conex = tipo_conex
        self.v_nom1 = v_nom1
        self.v_nom2 = v_nom2
        self.i_nom1 = i_nom1
        self.i_nom2 = i_nom2