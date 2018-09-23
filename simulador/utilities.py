# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.forms import ClearableFileInput, CheckboxInput
from django.shortcuts import redirect
from django.utils.html import format_html, conditional_escape
from django.utils.safestring import mark_safe
from datetime import datetime


from datetimewidget.widgets import DateWidget

from django.core.mail.backends import smtp

# Decorador que verifica que el usuario tenga alguno de los cargos permitidos
def verificar_rol(roles_permitidos):
	def _method_wrapper(view_method):
		def _arguments_wrapper(request, *args, **kwargs):
			request_inicial = request
			if hasattr(request,"request"): # Es una CBV
				request = request.request

			try:
				try:
					rol = request.session['rol_usuario']
				except KeyError:
					try:
						rol = request.user.groups.all()[0].name
						request.session['rol_usuario'] = rol
					except IndexError:
						messages.error(request, "Para acceder a la página solicitada requiere loguearse")
						return redirect('usuario:login')
				if not (rol in roles_permitidos):
					messages.error(request, "Usted no tiene permisos para acceder a la página solicitada")
					return redirect('inicio')
			except AttributeError:
				messages.error(request, "Para acceder a la página solicitada requiere loguearse")
				return redirect('usuario:login')

			return view_method(request_inicial, *args, **kwargs)
		return _arguments_wrapper
	return _method_wrapper