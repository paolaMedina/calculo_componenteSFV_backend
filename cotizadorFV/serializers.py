from rest_framework import serializers
from models import *

        
class CharField(serializers.CharField):
    def to_representation(self, value):
        utf8_value = value.decode('utf-8')
        return super(CharField, self).to_representation(utf8_value)
        

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
    isal_max_2= serializers.DecimalField(max_digits=50, decimal_places=2)
    isal_max_3= serializers.DecimalField(max_digits=50, decimal_places=2)
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
    
 
 
#______________________________Serializadores de interfaz______________________________________________  
    
class BaseCableadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseCableado
        fields='__all__'
        
class InputSerializer(serializers.ModelSerializer):
    input= BaseCableadoSerializer(required=True)
    class Meta:
        model = Input
        fields='__all__'
        
class OutputSerializer(serializers.ModelSerializer):
    output= BaseCableadoSerializer(required=True)
    class Meta:
        model = Output
        fields='__all__'
        
class CableadoSerializer(serializers.ModelSerializer):
    input= BaseCableadoSerializer(required=True)
    output=BaseCableadoSerializer(required=True)
    class Meta:
        model = Cableado
        fields='__all__'
    

    
    
class MpptSerializer(serializers.ModelSerializer):
    cableado=CableadoSerializer(required=True)
    class Meta:
        model = Mppt
        fields=('_id','nombre','numero_de_cadenas_en_paralelo','numero_de_paneles_en_serie_por_cadena','cableado')

       
class PanelFVSerializer(serializers.ModelSerializer):
    mttps=MpptSerializer(many=True, required=True)
    salida_inversor=OutputSerializer(required=True)
    
    class Meta:
        model = PanelFV
        fields=('_id','nombre','fabricante_1','model_panel_solar_1','modelo_panel_solar_2','fabricante_2','salida_inversor','mttps')

        
class GeneralFVSerializer(serializers.ModelSerializer):
    fvs=PanelFVSerializer(many=True, required=True)
    combinacion_inversor=InputSerializer(required=True)
    """
    def getGeneralFV(self):
        generalFV = None
        if self.is_valid():
            panelesFV = validated_data.pop('fvs')
            generalFV = GeneralFV(**validated_data)
            print(generalFV)
            return generalFV
    """        
    class Meta:
        model = GeneralFV
        fields=('potencia_de_planta_fv','nombre_proyecto','temperatura_ambiente','minima_temperatura_ambiente_esperada',
        'tipo_de_inversor','lugar_instalacion_opcion_techo_cubierta', 'tipo_servicio','voltage_servicio','lugar_instalacion',
        'combinacion_inversor','fvs')

  