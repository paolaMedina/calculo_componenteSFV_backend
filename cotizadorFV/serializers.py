from rest_framework import serializers
from models_form.generalFV import GeneralFVForm


class GeneralFVSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralFVForm
        fields = ('power_of_plant_fv', 'total_panels_fv', 'power_of_panel_fv', 'ambient_temperature', 'lowest_ambient_temperature_expected',
        'investment_type', 'service_type', 'service_voltage', 'instalation_place')

class Example:
    def __init__(self, a, b):
        self.a = a
        "attribute Example.a doc-string (1)"
        self.b = b
        "attribute Example.b doc-string (2)"
class ExampleSerializer(serializers.Serializer):
    a = serializers.CharField()
    b = serializers.CharField()
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
