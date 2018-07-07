
from adaptor.model import CsvModel
from adaptor.fields import CharField, IntegerField, DecimalField, DateField,FloatField
from decimal import Decimal
#Modelos de los excel

class DecimalField(DecimalField):
    def to_python(self, value):
        if (value==''):
            point_separated_decimal = 0
        else:
            point_separated_decimal = value.replace(',','.')
        return Decimal(point_separated_decimal)    
        
        
class InterruptorManual(CsvModel):
    descripcion= CharField()
    marca= CharField()
    referencia= CharField()
    aplicacion= CharField()
    ith= IntegerField()
    tension= IntegerField()
    no_contactos= IntegerField()
    tipo_montaje= CharField()
    precio= IntegerField()
    class Meta:
        delimiter = ";"
        has_header=True
        
        

class DpsAC(CsvModel):
    
    descripcion= CharField()
    marca= CharField()
    referencia= CharField()
    tipo= IntegerField()
    clase_prueba= CharField()
    forma_constructiva= CharField()
    no_polos= IntegerField()
    uc= IntegerField()
    in_in= IntegerField()
    imax_por_polo= CharField()
    iimp_por_polo= CharField()
    up=DecimalField()
    telesenal= CharField()
    precio= IntegerField()
    class Meta:
        delimiter = ";"
        has_header=True

        
class DpsDC(CsvModel):
     descripcion= CharField()
     marca= CharField()
     referencia= CharField()
     tipo= CharField()
     aplicacion= CharField()
     forma_constructiva= CharField()
     no_polos= CharField()
     uc= IntegerField()
     in_in= DecimalField()
     imax= IntegerField()
     precio= IntegerField()
     class Meta:
         delimiter = ";"
         has_header=True

class Fusible(CsvModel):
    descripcion=  CharField()
    marca= CharField()
    referencia= CharField()
    aplicacion= CharField()
    in_in = IntegerField()
    tension = IntegerField()
    ir= IntegerField()
    dimensiones= CharField()
    tipo= CharField()
    clase= CharField()
    precio= IntegerField()
    class Meta:
        delimiter = ";"  
        has_header=True
    
    
class InteAuto(CsvModel):
    descripcion= CharField()
    marca= CharField()
    referencia= CharField()
    aplicacion= CharField()
    tipo_tam= CharField()
    no_polos= IntegerField()
    no_polos_letras= CharField()
    tension= IntegerField()
    tension_2= IntegerField()
    in_in= IntegerField()
    icn= IntegerField()
    icn_2= CharField()
    precio= IntegerField()
    class Meta:
        delimiter = ";"    
        has_header=True
        
        
class Inversor(CsvModel):
    descripcion= CharField()
    modelo= CharField()
    fabricante= CharField()
    no_mppt= IntegerField()
    pot_nom= DecimalField()
    pot_fv_in_min= DecimalField()
    pot_fv_in_max= DecimalField()
    imax_in_mppt1= DecimalField()
    imax_in_mppt2= DecimalField()
    imax_in_mpptCombinado= CharField()
    iscmax_mppt1= DecimalField()
    iscmax_mppt2= DecimalField()
    iscmax_mppt3= CharField()
    iscmax_mpptCombinado= CharField()
    vin_min= IntegerField()
    vin_max= IntegerField()
    vop_min= IntegerField()
    vop_max= IntegerField()
    vsal_1= IntegerField()
    vsal_2= CharField()
    vsal_3= CharField()
    tipo_conex= CharField()
    psal_1= IntegerField()
    psal_2= CharField()
    pot_sal_3= CharField()
    isal_max_1= DecimalField()
    isal_max_2= CharField()
    isal_max_3= CharField()
    i_int_sal_1= DecimalField()
    i_int_sal_2= CharField()
    i_int_sal_3= CharField()
    class Meta:
        delimiter = ";"   
        has_header=True

class MicroInversor(CsvModel):
    descripcion= CharField()
    modelo= CharField()
    fabricante= CharField()
    pot_fv_in_min= IntegerField()
    pot_fv_in_max= IntegerField()
    vin_min= IntegerField()
    vin_max= IntegerField()
    vop_min= IntegerField()
    vop_max= IntegerField()
    vreg_min= IntegerField()
    vreg_max= IntegerField()
    isc_max= IntegerField()
    psal_max= IntegerField()
    psal_nom= IntegerField()
    tipo_conex= CharField()
    v_nom1= IntegerField()
    v_nom2= IntegerField()
    i_nom1= DecimalField()
    i_nom2= DecimalField()
    class Meta:
        delimiter = ";"   
        has_header=True
        
        
class PanelSolar(CsvModel):
    
    descripcion= CharField()
    modelo= CharField()
    fabricante= CharField()
    tipo_celda= CharField()
    no_de_celdas= CharField()
    pmax= CharField()
    eficiencia= CharField()
    vmpp= CharField()
    impp= DecimalField()
    voc= DecimalField()
    isc= DecimalField()
    coef_voc= CharField()
    class Meta:
        delimiter = ";"
        has_header = True
