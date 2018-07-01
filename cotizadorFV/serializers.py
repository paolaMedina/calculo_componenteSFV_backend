

from rest_framework import serializers
from models_form.generalFV import GeneralFVForm
from models_excel.dps_ac import DpsAC
from models_excel.dps_dc import DpsDC


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
    

    def create(self, validated_data):
        """
        Crea y devuelve una nueva instancia de 'DpsAC', dados los datos validados.
        """
        return DpsAC.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza y devuelva una instancia existente de 'DpsAC', dados los datos validados..
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        
        instance.descripcion = validated_data.get('descripcion', instance.descripcion )
        instance.marca = validated_data.get('marca', instance.marca )
        instance.referencia = validated_data.get('referencia', instance.referencia)
        instance.tipo = validated_data.get('tipo', instance.tipo)
        instance.clase_prueba = validated_data.get('clase_prueba', instance.clase_prueba)
        instance.forma_constructiva = validated_data.get('forma_constructiva', instance.forma_constructiva)
        instance.no_polos = validated_data.get('no_polos', instance.no_polos)
        instance.uc = validated_data.get('uc', instance.uc)
        instance.in_in = validated_data.get('in_in', instance.in_in)
        instance.imax_por_polo = validated_data.get('imax_por_polo', instance.imax_por_polo)
        instance.iimp_por_polo = validated_data.get('iimp_por_polo', instance.iimp_por_polo)
        instance.up = validated_data.get('up', instance.up)
        instance.telesenal = validated_data.get('telesenal', instance.telesenal)
        instance.precio = validated_data.get('precio', instance.precio)
        instance.save()
        return instance
        
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
     # no hace falta por que no se va a guardar en la bd
     def create(self, validated_data):
         return DpsDC.objects.create(**validated_data)
