# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.views.generic.edit import FormView
from .forms import FormUpload
from django.core.urlresolvers import reverse_lazy
 
 
class UploadFileView(FormView):
    '''
    Esta vista sube un archivo al servidor
    '''
    template_name = "index.html"
    form_class = FormUpload
    success_url = reverse_lazy("cargarArchivos:index")
 
    def get(self, request, *args, **kwargs):
        
 
        data = {'form': self.form_class}
 
        return render(request, self.template_name, data)
 
    def post(self, request, *args, **kwargs):
        form = FormUpload(request.POST, request.FILES)
        print(request.FILES['file'])
        file = request.FILES['file']
        for chunk in file.chunks():
            print(chunk)
        print "eyy"
        if form.is_valid():
            print "entre"
            if 'file' in request.FILES:
                file = request.FILES['file']
                form.handle_uploaded_file(file)
                return self.form_valid(form, **kwargs)
                
            else:
                return self.form_invalid(form, **kwargs)
        else:
            print form.errors
            return self.form_invalid(form, **kwargs)
