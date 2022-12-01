from django.shortcuts import render
from ejemplo.models import Familiar

def index(request):
    return render(request, "ejemplo/saludar.html")


def saludar_a(request, nombre):
    return render(request,
    'ejemplo/saludar_a.html',
    {'nombre': nombre})

def monstrar_familiares(request):
      lista_familiares = Familiar.objects.all()
      return render(request, "ejemplo/familiares.html", {"lista_familiares": lista_familiares})
  
def buscar(request):
    lista_de_nombre = ["german", "daniel", "romero", "alvaro"]
    query = request.GET['q']
    
    indice_de_resultado = lista_de_nombre.index(query)
    
    return render(request, 'ejemplo/buscar.html', {"resultado": lista_de_nombre [indice_de_resultado]})