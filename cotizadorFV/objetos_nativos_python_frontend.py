# -*- coding: utf-8 -*-

class Generalfv():
    def __init__(self, potencia_de_planta_fv,nombre_proyecto,
        temperatura_ambiente,minima_temperatura_ambiente_esperada,tipo_de_inversor,
        lugar_instalacion_opcion_techo_cubierta, tipo_servicio,voltage_servicio,lugar_instalacion,fvs=[]):
    
        self.potencia_de_planta_fv = potencia_de_planta_fv
        self.nombre_proyecto = nombre_proyecto
        self.temperatura_ambiente = temperatura_ambiente
        self.minima_temperatura_ambiente_esperada = minima_temperatura_ambiente_esperada
        self.tipo_de_inversor = tipo_de_inversor
        self.lugar_instalacion_opcion_techo_cubierta = lugar_instalacion_opcion_techo_cubierta
        self.tipo_servicio = tipo_servicio
        self.voltage_servicio = voltage_servicio
        self.lugar_instalacion = lugar_instalacion
        self.fvs= [PanelFV(**fv) for fv in fvs]

    
    
class PanelFV():
    def __init__(self,_id,nombre,fabricante_1,model_panel_solar_1,modelo_panel_solar_2,fabricante_2,salida_inversor,mttps=[]):
        self._id = _id
        self.nombre = nombre
        self.fabricante_1 = fabricante_1#fabricante panel
        self.model_panel_solar_1 = model_panel_solar_1#modelo panel
        self.modelo_panel_solar_2 = modelo_panel_solar_2#modelo inversor
        self.fabricante_2 = fabricante_2#fabricante inversor
        self.mttps  =  [Mttp(**mttp) for mttp in mttps]
        self.salida_inversor =Cableado (**salida_inversor)#BaseCableado(**salida_inversor)
    
    
    
class Mttp():
    def __init__(self,_id,nombre,numero_de_cadenas_en_paralelo,numero_de_paneles_en_serie_por_cadena,cableado):
        self._id = _id
        self.nombre = nombre
        self.numero_de_cadenas_en_paralelo = numero_de_cadenas_en_paralelo
        self.numero_de_paneles_en_serie_por_cadena = numero_de_paneles_en_serie_por_cadena
        self.cableado = Cableado (**cableado)
        

class Cableado():
    def __init__(self,input, output):
        self.input= BaseCableado(**input)
        self.output= BaseCableado(**output)
        
        
class BaseCableado():
    def __init__(self,_id,tipo_alambrado,tipo_conductor,distancia_del_conductor_mas_largo,caida_de_tension_de_diseno,tipo_canalizacion,
                canalizacion,tamanio_canalizacion,material_conductor,disenio_bandeja,material_bandeja,tipo_acabado,
                tapa_superior_bandeja_portacable,tapa_inferior_bandeja_portacable,perfiles_separadores,longitud_tramo,
                ancho_mm,maximo_numero_de_conductores,alto_mm,tipo_carga):
        self._id=_id
        self.tipo_alambrado=tipo_alambrado
        self.tipo_conductor=tipo_conductor
        self.distancia_del_conductor_mas_largo=distancia_del_conductor_mas_largo
        self.caida_de_tension_de_diseno=caida_de_tension_de_diseno
        self.tipo_canalizacion=tipo_canalizacion
        self.canalizacion=canalizacion
        self.tamanio_canalizacion=tamanio_canalizacion
        self.material_conductor=material_conductor
        self.disenio_bandeja=disenio_bandeja
        self.material_bandeja=material_bandeja
        self.tipo_acabado=tipo_acabado
        self.tapa_superior_bandeja_portacable=tapa_superior_bandeja_portacable
        self.tapa_inferior_bandeja_portacable=tapa_inferior_bandeja_portacable
        self.perfiles_separadores=perfiles_separadores
        self.longitud_tramo=longitud_tramo
        self.ancho_mm=ancho_mm
        self.maximo_numero_de_conductores=maximo_numero_de_conductores
        self.alto_mm=alto_mm
        self.tipo_carga=tipo_carga