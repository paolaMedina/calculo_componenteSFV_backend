from django import forms
 
from .widgets import KrajeeFileInputWidget
from django.core.exceptions import ValidationError

class FormUpload(forms.Form):
    
    archivos= (
    ('dps_ac', 'DPS_AC'),
    ('dps_dc', 'DPS.DC'),
    ('fusible', 'Fusibles'),
    ('inte_auto', 'Interrupturos Automaticos'),
    ('inte_man',  'Interrupturos Manuales'),
    ('inversor', 'Inversores'),
    ('microInve', 'MicroInversores'),
    ('panelSolar', 'Paneles Solares'),
    )
    '''
    Form principal
    '''
    #file = forms.FileField(widget= KrajeeFileInputWidget )
    tipo_archivo=forms.ChoiceField(choices=archivos,label='Tipo de archivo',widget=forms.Select(attrs={'class':'form-control', 'required':'required'}))
    file = forms.FileField( )
    
    