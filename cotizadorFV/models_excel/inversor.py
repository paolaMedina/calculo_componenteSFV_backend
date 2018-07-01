
 class Inversor:

	def __init__(self,descripcion , modelo , fabricante , no_mppt , pot_nom , pot_fv_in_min , pot_fv_in_max , imax_in_mppt1 , 
		imax_in_mppt2 , imax_in_mpptCombinado , imax_in_mppt3 , iscmax_mppt1 , iscmax_mppt2 , iscmax_mppt3 , iscmax_mpptCombinado , 
		vin_min , vin_max , vop_min , vop_max , vsal_1 , vsal_2 , vsal_3 , tipo_conex , psal_1 , psal_2 , pot_sal_3 , isal_max_1 , 
		isal_max_2 , isal_max_3 , i_int_sal_1 , i_int_sal_2 , i_int_sal_3 ):
		self.descripcion = descripcion
		self.modelo = modelo
		self.fabricante = fabricante
		self.no_mppt = no_mppt
		self.pot_nom = pot_nom
		self.pot_fv_in_min = pot_fv_in_min
		self.pot_fv_in_max = pot_fv_in_max
		self.imax_in_mppt1 = imax_in_mppt1
		self.imax_in_mppt2 = imax_in_mppt2
		self.imax_in_mpptCombinado = imax_in_mpptCombinado
		self.imax_in_mppt3 = imax_in_mppt3
		self.iscmax_mppt1 = iscmax_mppt1
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
	
