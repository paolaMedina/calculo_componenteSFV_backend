# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from datetime import datetime
 
# Create your models here.
administrador='administrador'
ingeniero='ingeniero'
cotizador= 'cotizador'

grupos = ((administrador, 'Administrador'), (cotizador, 'Cotizador'),(ingeniero, 'Ingeniero'))


class Usuario(User):
    identificacion= models.IntegerField()
    rol=models.CharField(max_length=24, choices=grupos, default='cotizador')
    imagen = models.ImageField(upload_to='avatar/', null=True, blank=True)

    def __unicode__(self,):
        return str(self.imagen)
    




