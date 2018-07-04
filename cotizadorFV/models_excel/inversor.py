
class Inversor:
    def __init__(self, descripcion = None,  modelo = None,  fabricante = None,  no_mppt = None,  pot_nom = None,  pot_fv_in_min = None,  pot_fv_in_max = None,  imax_in_mppt1 = None,  
		imax_in_mppt2 = None,  imax_in_mpptCombinado = None,  imax_in_mppt3 = None,  iscmax_mppt1 = None,  iscmax_mppt2 = None,  iscmax_mppt3 = None,  iscmax_mpptCombinado = None,  
		vin_min = None,  vin_max = None,  vop_min = None,  vop_max = None,  vsal_1 = None,  vsal_2 = None,  vsal_3 = None,  tipo_conex = None,  psal_1 = None,  psal_2 = None,  pot_sal_3 = None,  isal_max_1 = None,  
		isal_max_2 = None,  isal_max_3 = None, imax_in_mppt1_i= None, iscmax_mppt1_2= None,  imax_in_mppt1_ii= None,  i_int_sal_1 = None,  i_int_sal_2 = None,  i_int_sal_3=None):
		self.descripcion = descripcion
		self.modelo = modelo
		self.fabricante = fabricante
		self.no_mppt = no_mppt
		self.pot_nom = pot_nom
		self.pot_fv_in_min = pot_fv_in_min
		self.pot_fv_in_max = pot_fv_in_max
		self.imax_in_mppt1 = imax_in_mppt1
		self.imax_in_mppt1_i = imax_in_mppt1_i
		self.imax_in_mppt1_ii = imax_in_mppt1_ii
		self.imax_in_mppt2 = imax_in_mppt2
		self.imax_in_mpptCombinado = imax_in_mpptCombinado
		self.imax_in_mppt3 = imax_in_mppt3
		self.iscmax_mppt1 = iscmax_mppt1
		self.iscmax_mppt1_2 = iscmax_mppt1_2
		self.iscmax_mppt2 = iscmax_mppt2
		self.iscmax_mppt3 = iscmax_mppt3
		self.iscmax_mpptCombinado = iscmax_mpptCombinado
		self.vin_min = vin_min
		self.vin_max = vin_max
		self.vop_min = vop_min
		self.vop_max = vop_max
		self.vsal_1 = vsal_1
		self.vsal_2 = vsal_2
		self.vsal_3 = vsal_3
		self.tipo_conex = tipo_conex
		self.psal_1 = psal_1
		self.psal_2 = psal_2
		self.pot_sal_3 = pot_sal_3
		self.isal_max_1 = isal_max_1
		self.isal_max_2 = isal_max_2
		self.isal_max_3 = isal_max_3
		self.i_int_sal_1 = i_int_sal_1
		self.i_int_sal_2 = i_int_sal_2
		self.i_int_sal_3 = i_int_sal_3
	
