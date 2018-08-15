# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#Importamos la vista generica FormView
from django.views.generic.edit import FormView
from django.http.response import HttpResponseRedirect
from django.contrib.auth import login
from django.shortcuts import render,get_object_or_404, render_to_response
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.contrib.messages.views import SuccessMessageMixin
import hashlib, datetime, random
from django.utils import timezone
from .forms import RegistroForm,UpdateForm,FormularioLogin
from .models import Usuario
from simulador.utilities import *
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class RegistroUsuario(LoginRequiredMixin,CreateView):
    template_name = "registrar.html"
    success_url=reverse_lazy("usuario:registrar_usuario")
    model = Usuario
    form_class = RegistroForm
             
    """
    @verificar_rol(roles_permitidos=["administrador"])
    def dispatch(self, request, *args, **kwargs):
        return super(RegistroUsuario, self).dispatch(request, *args, **kwargs)
    """    
   
    
    def form_valid(self, form):
        usuario= form.instance
        #contrasena con la inicial del nombre en mayuscula, la identificacion y la inicial del apellido en mayuscula
        contra= usuario.first_name[0].upper()+str(usuario.identificacion)+usuario.last_name[0].upper()
        usuario.password1=contra
        
        email = form.cleaned_data['email']
        
        # Enviar un email de confirmacion
        email_subject = 'Account confirmation'
        email_body = "Buenas acabas de ser registrado en la pagina de © Solar Energies. Tus datos de registro son: \n Usuario:%s \n contrasena es %s \n puedes ingresar al siguiente link para loguearte: https://simulador-fv-paolamedina.c9users.io/usuario/" % (usuario.username,usuario.password1)
        
        send_mail(email_subject, email_body, 'angiepmc93@gmail.com',
            [email], fail_silently=False)
        
        self.object = form.save(commit=False)
        self.object.set_password(contra)
        
        if (usuario.imagen==None):
            self.object.imagen="/avatar/user.png"
            
        self.object.save()
        
        #agrupar usuario dependiendo su rol
        if (usuario.rol=='administrador'):
            grupo_director, grupo_director_creado = Group.objects.get_or_create(name='administrador')
            grupo_director.user_set.add(self.object)
        elif (usuario.rol=='ingeniero'):
            grupo_investigador, grupo_investigador_creado = Group.objects.get_or_create(name='ingeniero')
            grupo_investigador.user_set.add(self.object)
        elif (usuario.rol=='cotizador'):
            grupo_curador, grupo_curador_creado = Group.objects.get_or_create(name='cotizador')
            grupo_curador.user_set.add(self.object)
            
        messages.success(self.request, 'Se agrego el usuario con EXITO')
        return super(RegistroUsuario, self).form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'hay uno o mas campos invalidos. Por favor verifique de nuevo')
        print form.errors
        return  super(RegistroUsuario, self).form_invalid(form)
        

               
class ListarUsuarios(LoginRequiredMixin,ListView):
    """
    @verificar_rol(roles_permitidos=["administrador"])
    def dispatch(self, request, *args, **kwargs):
        return super(ListarUsuarios, self).dispatch(request, *args, **kwargs)
    """    
    model=Usuario
    template_name='listar.html'
    
    
       
class EditarUsuario(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    """
    @verificar_rol(roles_permitidos=["administrador"])
    def dispatch(self, request, *args, **kwargs):
        return super(EditarUsuario, self).dispatch(request, *args, **kwargs)
    """    
   
    model = Usuario
    form_class = UpdateForm
    template_name = "registrar.html"
    success_url=reverse_lazy("usuario:listar_usuario")
    success_message='Se  edito con EXITO'
  

class EliminarUsuario(LoginRequiredMixin,DeleteView):
    """
    @verificar_rol(roles_permitidos=["administrador"])
    def dispatch(self, request, *args, **kwargs):
        return super(EliminarUsuario, self).dispatch(request, *args, **kwargs)
    """    
    model = Usuario
    success_url=reverse_lazy("usuario:listar_usuario")
    success_message = 'Se elimino el usuario con EXITO'
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EliminarUsuario, self).delete(request, *args, **kwargs) 
        
    #funcion para no ingresar template de confirmacion delete
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
        
        

class Login(FormView):
    template_name = 'login.html'
    form_class = FormularioLogin 
    success_url =  reverse_lazy('inicio')
 
    def dispatch(self, request, *args, **kwargs):
        #Si el usuario esta autenticado entonces nos direcciona a la url establecida en success_url
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        #Sino lo esta entonces nos muestra la plantilla del login simplemente
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)
 
    def form_valid(self, form):
        login(self.request, form.get_user())
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        return super(Login, self).form_valid(form)
        
    def form_invalid(self, form):
        print "invalid"
        messages.error(self.request, 'NOMBRE DE USUARIO O CONTRASEÑA INCORRECTAS')
        print form.errors
        return  super(Login, self).form_invalid(form)