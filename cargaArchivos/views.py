# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import FormUpload
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
import os
 
class UploadFileView(FormView):
    '''
    Esta vista sube un archivo al servidor
    '''
    template_name = "upload.html"
    form_class = FormUpload
    success_url = reverse_lazy("cargarArchivos:index")
 
    def get(self, request, *args, **kwargs):
        data = {'form': self.form_class}
        return render(request, self.template_name, data)
 
    def post(self, request, *args, **kwargs):
        form = FormUpload(request.POST, request.FILES)
        
        if form.is_valid():
            # se convierte el form a un diccionario, y se obtiene el atributo
            type = form.cleaned_data.get('tipo_archivo')
            name=''
            file = request.FILES['file']
            extension = os.path.splitext(file.name)[1]
            print extension
            if 'file' in request.FILES and extension=='.csv':
                if (type == 'dps_ac'):
                    name='DPS_AC.csv'
                elif (type == 'dps_dc'):
                    name='DPS_DC.csv'
                elif (type == 'fusible'):
                    name='fusibles.csv'
                elif (type == 'inte_auto'):
                    name='interruptores_automaticos.csv'
                elif (type == 'inte_man'):
                    name='interruptores_manuales.csv'
                elif (type == 'inversor'):
                    name='inversor.csv'
                elif (type == 'microInve'):
                    name='microinversor.csv'
                elif (type == 'panelSolar'):
                    name='panelesSolares.csv'
                    
                
                handle_uploaded_file(file,name)
                messages.success(self.request, 'Se actualizo el archivo '+ file.name +' con EXITO')
                return self.form_valid(form, **kwargs)
                
            else:
                return self.form_invalid(form, **kwargs)
               
        else:
            print form.errors
            return self.form_invalid(form, **kwargs)
            
            
            
def handle_uploaded_file(file,name):
        with open('archivos/' + name, 'w') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
                print chunk

