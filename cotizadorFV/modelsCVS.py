
from adaptor.model import CsvModel
from adaptor.fields import CharField, IntegerField, DecimalField, DateField,FloatField

#Modelos de los excel

class InterruptorManual(CsvModel):
    descripcion= CharField()
    marca= CharField()
    referencia= CharField()
    aplicacion= CharField()
    ith= CharField()
    tension= CharField()
    no_contactos= CharField()
    tipo_montaje= CharField()
    precio= CharField()
    class Meta:
        delimiter = ";"
        
        

class DpsAC(CsvModel):
    
    descripcion= CharField()
    marca= CharField()
    referencia= CharField()
    tipo= CharField()
    clase_prueba= CharField()
    forma_constructiva= CharField()
    no_polos= CharField()
    uc= CharField()
    in_in= CharField()
    imax_por_polo= CharField()
    iimp_por_polo= CharField()
    up=CharField()
    telesenal= CharField()
    precio= CharField()
    class Meta:
        delimiter = ";"    

        
class DpsDC(CsvModel):
     descripcion= CharField()
     marca= CharField()
     referencia= CharField()
     tipo= CharField()
     aplicacion= CharField()
     forma_constructiva= CharField()
     no_polos= CharField()
     uc= CharField()
     in_in= CharField()
     imax= CharField()
     precio= CharField()
     class Meta:
         delimiter = ";"

class Fusible(CsvModel):
    descripcion=  CharField()
    marca= CharField()
    referencia= CharField()
    aplicacion= CharField()
    in_in = CharField()
    tension = CharField()
    ir= CharField()
    dimensiones= CharField()
    tipo= CharField()
    clase= CharField()
    precio= CharField()
    class Meta:
        delimiter = ";"    
    
    
class InteAuto(CsvModel):
    descripcion= CharField()
    marca= CharField()
    referencia= CharField()
    aplicacion= CharField()
    tipo_tam= CharField()
    no_polos= CharField()
    no_polos_letras= CharField()
    tension= CharField()
    tension_2= CharField()
    in_in= CharField()
    icn= CharField()
    icn_2= CharField()
    precio= CharField()
    class Meta:
        delimiter = ";"    
class Inversor(CsvModel):
    descripcion= CharField()
    modelo= CharField()
    fabricante= CharField()
    no_mppt= CharField()
    pot_nom= CharField()
    pot_fv_in_min= CharField()
    pot_fv_in_max= CharField()
    imax_in_mppt1= CharField()
    imax_in_mppt2= CharField()
    imax_in_mpptCombinado= CharField()
    iscmax_mppt1= CharField()
    iscmax_mppt2= CharField()
    iscmax_mppt3= CharField()
    iscmax_mpptCombinado= CharField()
    vin_min= CharField()
    vin_max= CharField()
    vop_min= CharField()
    vop_max= CharField()
    vsal_1= CharField()
    vsal_2= CharField()
    vsal_3= CharField()
    tipo_conex= CharField()
    psal_1= CharField()
    psal_2= CharField()
    pot_sal_3= CharField()
    isal_max_1= CharField()
    isal_max_2= CharField()
    isal_max_3= CharField()
    i_int_sal_1= CharField()
    i_int_sal_2= CharField()
    i_int_sal_3= CharField()
    class Meta:
        delimiter = ";"   

class MicroInversor(CsvModel):
    descripcion= CharField()
    modelo= CharField()
    fabricante= CharField()
    pot_fv_in_min= CharField()
    pot_fv_in_max= CharField()
    vin_min= CharField()
    vin_max= CharField()
    vop_min= CharField()
    vop_max= CharField()
    vreg_min= CharField()
    vreg_max= CharField()
    isc_max= CharField()
    psal_max= CharField()
    psal_nom= CharField()
    tipo_conex= CharField()
    v_nom1= CharField()
    v_nom2= CharField()
    i_nom1= CharField()
    i_nom2= CharField()
    class Meta:
        delimiter = ";"   
class PanelSolar(CsvModel):
    
    descripcion= CharField()
    modelo= CharField()
    fabricante= CharField()
    tipo_celda= CharField()
    no_de_celdas= CharField()
    pmax= CharField()
    eficiencia= CharField()
    vmpp= CharField()
    impp= CharField()
    voc= CharField()
    isc= CharField()
    coef_voc= CharField()
    class Meta:
        delimiter = ";"
