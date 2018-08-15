from __future__ import unicode_literals

from django.db import models

# Create your models here.




    
#modelo de del formulario principal 
class GeneralFV(models.Model):
    potencia_de_planta_fv = models.DecimalField(max_digits=50, decimal_places=2)
    nombre_proyecto = models.CharField(max_length= 255)
    temperatura_ambiente =  models.IntegerField()
    minima_temperatura_ambiente_esperada = models.IntegerField()
    tipo_de_inversor = models.CharField(max_length = 40)
    lugar_instalacion_opcion_techo_cubierta = models.CharField(max_length = 40,null=True)
    tipo_servicio = models.CharField(max_length = 40)
    voltage_servicio = models.CharField(max_length = 40)
    lugar_instalacion = models.CharField(max_length = 40)
    combinacion_inversor= models.ForeignKey('Input')
    class Meta:
        managed = False
        
        
        
#modelo panel fv
class PanelFV(models.Model):
    general= models.ForeignKey('GeneralFV')
    _id = models.CharField(max_length = 255)
    nombre = models.CharField(max_length = 40)
    fabricante_1 =models.CharField(max_length = 40)
    model_panel_solar_1 = models.CharField(max_length = 40)
    modelo_panel_solar_2 = models.CharField(max_length = 40)
    fabricante_2 = models.CharField(max_length = 40)
    salida_inversor= models.ForeignKey('Output')
    class Meta:
        managed = False
        
#modelo mppt

class Mppt(models.Model):
    panel = models.ForeignKey('PanelFV')
    _id = models.CharField(max_length = 255)
    nombre = models.CharField(max_length = 255)
    numero_de_cadenas_en_paralelo = models.IntegerField()
    numero_de_paneles_en_serie_por_cadena = models.IntegerField()
    cableado = models.ForeignKey('Cableado')
    class Meta:
        managed = False
        


class BaseCableado(models.Model):

    _id= models.CharField(max_length = 255)
    tipo_alambrado= models.CharField(max_length = 40)
    tipo_conductor= models.CharField(max_length = 40,null=True)
    distancia_del_conductor_mas_largo= models.IntegerField()
    caida_de_tension_de_diseno= models.IntegerField()
    tipo_canalizacion= models.CharField(max_length = 40,null=True)
    canalizacion= models.CharField(max_length = 40,null=True)
    tamanio_canalizacion= models.CharField(max_length = 40,null=True)
    material_conductor= models.CharField(max_length = 40)
    disenio_bandeja= models.CharField(max_length = 40,null=True)
    material_bandeja= models.CharField(max_length = 40,null=True)
    tipo_acabado= models.CharField(max_length = 40,null=True)
    tapa_superior_bandeja_portacable= models.NullBooleanField(null=True) 
    tapa_inferior_bandeja_portacable= models.NullBooleanField(null=True) 
    perfiles_separadores= models.NullBooleanField(null=True) 
    longitud_tramo= models.CharField(max_length = 40,null=True) 
    ancho_mm= models.CharField(max_length = 40,null=True)
    maximo_numero_de_conductores= models.IntegerField()
    alto_mm= models.CharField(max_length = 40,null=True)
    tipo_carga= models.CharField(max_length = 40,null=True)

class Cableado(models.Model):
    input= models.ForeignKey('BaseCableado', related_name='fuente')
    output= models.ForeignKey('BaseCableado',related_name='salida')


class Input(models.Model):
    input= models.ForeignKey('BaseCableado')
        
        
class Output(models.Model):
    output= models.ForeignKey('BaseCableado')

        
        
        

