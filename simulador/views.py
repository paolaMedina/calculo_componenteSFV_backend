

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.core.urlresolvers import reverse_lazy


def Home(request):
    return render(request, 'index2.html')
    
    
def loginPage(request):
    return  redirect('usuario:login')