from rest_framework import serializers
from models_form.generalFV import GeneralFVForm

        
class CharField(serializers.CharField):
    def to_representation(self, value):
        utf8_value = value.decode('utf-8')
        return super(CharField, self).to_representation(utf8_value)
        
class GeneralFVSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralFVForm
        fields = ('power_of_plant_fv', 'total_panels_fv', 'power_of_panel_fv', 'ambient_temperature', 'lowest_ambient_temperature_expected',
        'investment_type', 'service_type', 'service_voltage', 'instalation_place')


class DpsACSerializer(serializers.Serializer):
    
    descripcion= CharField(max_length=100)
    marca= CharField(max_length=100)
    referencia= CharField(max_length=100)
    tipo= serializers.IntegerField()
    clase_prueba= CharField(max_length=100)
    forma_constructiva= CharField(max_length=100)
    no_polos= serializers.IntegerField()
    uc= serializers.IntegerField()
    in_in= serializers.IntegerField()
    imax_por_polo= CharField(max_length=100)
    iimp_por_polo= CharField(max_length=100)
    up=serializers.DecimalField(max_digits=50, decimal_places=2)
    telesenal= CharField(max_length=100)
    precio= serializers.IntegerField()
    

        
class DpsDCSerializer(serializers.Serializer):
     descripcion= CharField(max_length=100)
     marca= CharField(max_length=100)
     referencia= CharField(max_length=100)
     tipo= CharField(max_length=100)
     aplicacion= CharField(max_length=100)
     forma_constructiva= CharField(max_length=100)
     no_polos= CharField(max_length=100)
     uc= serializers.IntegerField()
     in_in= serializers.DecimalField(max_digits=50, decimal_places=2)
     imax= serializers.IntegerField()
     precio= serializers.IntegerField()


class FusibleSerializer(serializers.Serializer):
    descripcion=  CharField(max_length=100)
    marca= CharField(max_length=100)
    referencia= CharField(max_length=100)
    aplicacion= CharField(max_length=100)
    in_in = serializers.IntegerField()
    tension = serializers.IntegerField()
    ir= serializers.IntegerField()
    dimensiones= CharField(max_length=100)
    tipo= CharField(max_length=100)
    clase= CharField(max_length=100)
    precio= serializers.IntegerField()
    
    
class InteAutoSerializer(serializers.Serializer):
    descripcion= CharField(max_length=100)
    marca= CharField(max_length=100)
    referencia= CharField(max_length=100)
    aplicacion= CharField(max_length=100)
    tipo_tam= CharField(max_length=100)
    no_polos= serializers.IntegerField()
    no_polos_letras= CharField(max_length=100)
    tension= serializers.IntegerField()
    tension_2= serializers.IntegerField()
    in_in= serializers.IntegerField()
    icn= serializers.IntegerField()
    icn_2= CharField(max_length=100)
    precio= serializers.IntegerField()
    
class InteManualSerializer(serializers.Serializer):
    descripcion= CharField(max_length=100)
    marca= CharField(max_length=100)
    referencia= CharField(max_length=100)
    aplicacion= CharField(max_length=100)
    ith= serializers.IntegerField()
    tension= serializers.IntegerField()
    no_contactos= serializers.IntegerField()
    tipo_montaje= CharField(max_length=100)
    precio= serializers.IntegerField()
    
class InversorSerializer(serializers.Serializer):
    descripcion= CharField(max_length=100)
    modelo= CharField(max_length=100)
    fabricante= CharField(max_length=100)
    no_mppt= serializers.IntegerField()
    pot_nom= serializers.DecimalField(max_digits=50, decimal_places=2)
    pot_fv_in_min= serializers.DecimalField(max_digits=50, decimal_places=2)
    pot_fv_in_max= serializers.DecimalField(max_digits=50, decimal_places=2)
    imax_in_mppt1= serializers.DecimalField(max_digits=50, decimal_places=2)
    imax_in_mppt2= serializers.DecimalField(max_digits=50, decimal_places=2)
    imax_in_mppt3= serializers.DecimalField(max_digits=50, decimal_places=2)
    imax_in_mppt4= serializers.DecimalField(max_digits=50, decimal_places=2)
    imax_in_mppt5= serializers.DecimalField(max_digits=50, decimal_places=2)
    imax_in_mppt6= serializers.DecimalField(max_digits=50, decimal_places=2)
    imax_in_mppt1_2= serializers.DecimalField(max_digits=50, decimal_places=2)
    imax_in_mppt3_4= serializers.DecimalField(max_digits=50, decimal_places=2)
    imax_in_mppt5_6= serializers.DecimalField(max_digits=50, decimal_places=2)
    iscmax_mppt1= serializers.DecimalField(max_digits=50, decimal_places=2)
    iscmax_mppt2= serializers.DecimalField(max_digits=50, decimal_places=2)
    iscmax_mppt3= serializers.DecimalField(max_digits=50, decimal_places=2)
    iscmax_mppt4= serializers.DecimalField(max_digits=50, decimal_places=2)
    iscmax_mppt5= serializers.DecimalField(max_digits=50, decimal_places=2)
    iscmax_mppt6= serializers.DecimalField(max_digits=50, decimal_places=2)
    iscmax_mppt1_2= serializers.DecimalField(max_digits=50, decimal_places=2)
    iscmax_mppt3_4= serializers.DecimalField(max_digits=50, decimal_places=2)
    iscmax_mppt5_6= serializers.DecimalField(max_digits=50, decimal_places=2)
    vin_min= serializers.IntegerField()
    vin_max= serializers.IntegerField()
    vop_min= serializers.IntegerField()
    vop_max= serializers.IntegerField()
    vsal_1= serializers.IntegerField()
    vsal_2= CharField(max_length=100)
    vsal_3= CharField(max_length=100)
    tipo_conex= CharField(max_length=100)
    psal_1= serializers.IntegerField()
    psal_2= CharField(max_length=100)
    pot_sal_3= CharField(max_length=100)
    isal_max_1= serializers.DecimalField(max_digits=50, decimal_places=2)
    isal_max_2= CharField(max_length=100)
    isal_max_3= CharField(max_length=100)
    i_int_sal_1= serializers.IntegerField()
    i_int_sal_2= CharField(max_length=100)
    i_int_sal_3= CharField(max_length=100)
    precio= serializers.IntegerField()
    

class MicroInversorSerializer(serializers.Serializer):
    descripcion= CharField(max_length=100)
    modelo= CharField(max_length=100)
    fabricante= CharField(max_length=100)
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
    tipo_conex= CharField(max_length=100)
    v_nom1= serializers.IntegerField()
    v_nom2= serializers.IntegerField()
    i_nom1= serializers.DecimalField(max_digits=50, decimal_places=2)
    i_nom2= serializers.DecimalField(max_digits=50, decimal_places=2)
    precio= serializers.IntegerField()
    
class PanelSolarSerializer(serializers.Serializer):
    
    descripcion= CharField(max_length=100)
    modelo= CharField(max_length=100)
    fabricante= CharField(max_length=100)
    tipo_celda= CharField(max_length=100)
    no_de_celdas= serializers.IntegerField()
    pmax= serializers.IntegerField()
    eficiencia= CharField(max_length=100)
    vmpp= serializers.DecimalField(max_digits=50, decimal_places=2)
    impp= serializers.DecimalField(max_digits=50, decimal_places=2)
    voc= serializers.DecimalField(max_digits=50, decimal_places=2)
    isc= serializers.DecimalField(max_digits=50, decimal_places=2)
    coef_voc= CharField(max_length=100)
    precio= serializers.IntegerField()
    
    

class DataSerializer(serializers.Serializer):
    dpssAC =  DpsACSerializer(many=True, required = True)
    dpssDC = DpsDCSerializer(many=True, required = True)
    fusibles = FusibleSerializer(many=True, required = True)
    interruptoresAutomaticos= InteAutoSerializer(many=True, required = True)
    interruptoresManuales = InteManualSerializer(many=True, required = True)
    inversores =InversorSerializer(many=True, required = True)
    microInversores = MicroInversorSerializer(many=True, required = True)
    panelesSolares = PanelSolarSerializer(many=True, required = True)    