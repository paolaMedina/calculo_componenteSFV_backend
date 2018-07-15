from django import forms
 
from .widgets import KrajeeFileInputWidget
from django.core.exceptions import ValidationError

class FormUpload(forms.Form):
 
    '''
    Form principal
    '''
    #file = forms.FileField(widget= KrajeeFileInputWidget )
    file = forms.FileField( )
    def handle_uploaded_file(self, f):
        print f.name
        with open('archivos/' + f.name, 'w') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
                print chunk
