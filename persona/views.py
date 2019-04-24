from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from .models import Persona
from .forms import PersonaForm
# Create your views here.
class IndexView(ListView):
    template_name = 'persona/index.html'
    model = Persona
    context_object_name = 'personas'

class PersonaRegistrar(CreateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'persona/ajax/registrar.html'

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, 'notificacion/success.html')

class PersonaEditar(UpdateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'persona/ajax/editar.html'
    context_object_name = 'persona'

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, 'notificacion/edited.html')