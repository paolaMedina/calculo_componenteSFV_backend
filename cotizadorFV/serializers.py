from rest_framework import serializers
from models_form.generalFV import GeneralFVForm



class GeneralFVSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralFVForm
        fields = ('power_of_plant_fv', 'total_panels_fv', 'power_of_panel_fv', 'ambient_temperature', 'lowest_ambient_temperature_expected',
        'investment_type', 'service_type', 'service_voltage', 'instalation_place')


class DpsACSerializer(serializers.Serializer):
    
    descripcion= serializers.CharField(max_length=100)
    marca= serializers.CharField(max_length=100)
    referencia= serializers.CharField(max_length=100)
    tipo= serializers.IntegerField()
    clase_prueba= serializers.CharField(max_length=100)
    forma_constructiva= serializers.CharField(max_length=100)
    no_polos= serializers.IntegerField()
    uc= serializers.IntegerField()
    in_in= serializers.IntegerField()
    imax_por_polo= serializers.CharField(max_length=100)
    iimp_por_polo= serializers.CharField(max_length=100)
    up=serializers.DecimalField(max_digits=50, decimal_places=25)
    telesenal= serializers.CharField(max_length=100)
    precio= serializers.CharField(max_length=100)
    

        
class DpsDCSerializer(serializers.Serializer):
     descripcion= serializers.CharField(max_length=100)
     marca= serializers.CharField(max_length=100)
     referencia= serializers.CharField(max_length=100)
     tipo= serializers.CharField(max_length=100)
     aplicacion= serializers.CharField(max_length=100)
     forma_constructiva= serializers.CharField(max_length=100)
     no_polos= serializers.CharField(max_length=100)
     uc= serializers.IntegerField()
     in_in= serializers.DecimalField(max_digits=50, decimal_places=25)
     imax= serializers.IntegerField()
     precio= serializers.CharField(max_length=100)


class FusibleSerializer(serializers.Serializer):
    descripcion=  serializers.CharField(max_length=100)
    marca= serializers.CharField(max_length=100)
    referencia= serializers.CharField(max_length=100)
    aplicacion= serializers.CharField(max_length=100)
    in_in = serializers.IntegerField()
    tension = serializers.IntegerField()
    ir= serializers.IntegerField()
    dimensiones= serializers.CharField(max_length=100)
    tipo= serializers.CharField(max_length=100)
    clase= serializers.CharField(max_length=100)
    precio= serializers.CharField(max_length=100)
    
    
class InteAutoSerializer(serializers.Serializer):
    descripcion= serializers.CharField(max_length=100)
    marca= serializers.CharField(max_length=100)
    referencia= serializers.CharField(max_length=100)
    aplicacion= serializers.CharField(max_length=100)
    tipo_tam= serializers.CharField(max_length=100)
    no_polos= serializers.IntegerField()
    no_polos_letras= serializers.CharField(max_length=100)
    tension= serializers.IntegerField()
    tension_2= serializers.IntegerField()
    in_in= serializers.IntegerField()
    icn= serializers.IntegerField()
    icn_2= serializers.CharField(max_length=100)
    precio= serializers.CharField(max_length=100)
    
class InteManualSerializer(serializers.Serializer):
    descripcion= serializers.CharField(max_length=100)
    marca= serializers.CharField(max_length=100)
    referencia= serializers.CharField(max_length=100)
    aplicacion= serializers.CharField(max_length=100)
    ith= serializers.IntegerField()
    tension= serializers.IntegerField()
    no_contactos= serializers.IntegerField()
    tipo_montaje= serializers.CharField(max_length=100)
    precio= serializers.CharField(max_length=100)
    
class InversorSerializer(serializers.Serializer):
    descripcion= serializers.CharField(max_length=100)
    modelo= serializers.CharField(max_length=100)
    fabricante= serializers.CharField(max_length=100)
    no_mppt= serializers.IntegerField()
    pot_nom= serializers.DecimalField(max_digits=50, decimal_places=25)
    pot_fv_in_min= serializers.DecimalField(max_digits=50, decimal_places=25)
    pot_fv_in_max= serializers.DecimalField(max_digits=50, decimal_places=25)
    imax_in_mppt1= serializers.IntegerField()
    imax_in_mppt2= serializers.DecimalField(max_digits=50, decimal_places=25)
    imax_in_mpptCombinado= serializers.CharField(max_length=100)
    iscmax_mppt1= serializers.DecimalField(max_digits=50, decimal_places=25)
    iscmax_mppt2= serializers.DecimalField(max_digits=50, decimal_places=25)
    iscmax_mppt3= serializers.CharField(max_length=100)
    iscmax_mpptCombinado= serializers.CharField(max_length=100)
    vin_min= serializers.IntegerField()
    vin_max= serializers.IntegerField()
    vop_min= serializers.IntegerField()
    vop_max= serializers.IntegerField()
    vsal_1= serializers.IntegerField()
    vsal_2= serializers.CharField(max_length=100)
    vsal_3= serializers.CharField(max_length=100)
    tipo_conex= serializers.CharField(max_length=100)
    psal_1= serializers.IntegerField()
    psal_2= serializers.CharField(max_length=100)
    pot_sal_3= serializers.CharField(max_length=100)
    isal_max_1= serializers.DecimalField(max_digits=50, decimal_places=25)
    isal_max_2= serializers.CharField(max_length=100)
    isal_max_3= serializers.CharField(max_length=100)
    i_int_sal_1= serializers.IntegerField()
    i_int_sal_2= serializers.CharField(max_length=100)
    i_int_sal_3= serializers.CharField(max_length=100)
    

class MicroInversorSerializer(serializers.Serializer):
    descripcion= serializers.CharField(max_length=100)
    modelo= serializers.CharField(max_length=100)
    fabricante= serializers.CharField(max_length=100)
    pot_fv_in_min= serializers.IntegerField()
    pot_fv_in_max= serializers.IntegerField()
    vin_min= serializers.IntegerField()
    vin_max= serializers.IntegerField()
    vop_min= serializers.IntegerField()
    vop_max= serializers.IntegerField()
    vreg_min= serializers.IntegerField()
    vreg_max= serializers.IntegerField()
    isc_max= serializers.IntegerField()
    psal_max= serializers.IntegerField()
    psal_nom= serializers.IntegerField()
    tipo_conex= serializers.CharField(max_length=100)
    v_nom1= serializers.IntegerField()
    v_nom2= serializers.IntegerField()
    i_nom1= serializers.CharField(max_length=100)
    i_nom2= serializers.CharField(max_length=100)
    
class PanelSolarSerializer(serializers.Serializer):
    
    descripcion= serializers.CharField(max_length=100)
    modelo= serializers.CharField(max_length=100)
    fabricante= serializers.CharField(max_length=100)
    tipo_celda= serializers.CharField(max_length=100)
    no_de_celdas= serializers.IntegerField()
    pmax= serializers.IntegerField()
    eficiencia= serializers.CharField(max_length=100)
    vmpp= serializers.DecimalField(max_digits=50, decimal_places=25)
    impp= serializers.CharField(max_length=100)
    voc= serializers.DecimalField(max_digits=50, decimal_places=25)
    isc= serializers.CharField(max_length=100)
    coef_voc= serializers.CharField(max_length=100)
    
    

class DataSerializer(serializers.Serializer):
    dpsAC =  DpsACSerializer()
    dpsDC = DpsDCSerializer
    fusible = FusibleSerializer
    interruptorAuto= InteAutoSerializer
    interruptorManual = InteManualSerializer
    inversor =InversorSerializer
    microInversor = MicroInversorSerializer
    panelSolar = PanelSolarSerializer