from django.shortcuts import render
from django.template import loader

def acceuil(request):
    return render(request,'acceuil.html' )