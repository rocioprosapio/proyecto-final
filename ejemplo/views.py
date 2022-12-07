from django.shortcuts import render, get_object_or_404 # <----- Nuevo import
from ejemplo.models import Familiar
from ejemplo.forms import Buscar, FamiliarForm # <--- NUEVO IMPORT
from django.views import View # <-- NUEVO IMPORT 

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

class BuscarFamiliar(View):
    form_class = Buscar
    template_name = 'ejemplo/buscar.html'
    initial = {"nombre":""}
    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form':form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data.get("nombre")
            lista_familiares = Familiar.objects.filter(nombre__icontains=nombre).all() 
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name, {'form':form, 
                                                        'lista_familiares':lista_familiares})
        return render(request, self.template_name, {"form": form})


class AltaFamiliar(View):
    
    form_class = FamiliarForm
    template_name = 'ejemplo/alta_familiar.html'
    initial = {"nombre":"", "direccion":"", "numero_pasaporte":""}

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            msg_exito = f"se cargo con éxito el familiar {form.cleaned_data.get('nombre')}"
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name, {'form':form, 
                                                        'msg_exito': msg_exito})
        
        return render(request, self.template_name, {"form": form})
    
    
class ActualizarFamiliar(View):
    form_class = FamiliarForm
    template_name = 'ejemplo/actualizar_familiar.html'
    initial = {"nombre":"", "direccion":"", "numero_pasaporte":""}
  
  # prestar atención ahora el method get recibe un parametro pk == primaryKey == identificador único
    def get(self, request, pk): 
      familiar = get_object_or_404(Familiar, pk=pk)
      form = self.form_class(instance=familiar)
      return render(request, self.template_name, {'form':form,'familiar': familiar})

  # prestar atención ahora el method post recibe un parametro pk == primaryKey == identificador único
    def post(self, request, pk): 
      familiar = get_object_or_404(Familiar, pk=pk)
      form = self.form_class(request.POST ,instance=familiar)
      if form.is_valid():
        form.save()
        msg_exito = f"se actualizó con éxito el familiar {form.cleaned_data.get('nombre')}"
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form':form, 
                                                    'familiar': familiar,
                                                    'msg_exito': msg_exito})
      
      return render(request, self.template_name, {"form": form})