from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import View
from django.db.models import Q
from django.http import JsonResponse
from .models import Persona
from .forms import PersonaForm
# Create your views here.
class PersonaAutocomplete(View):
    def get(self, *args, **kwargs):
        q = self.request.GET['q']
        qs = Persona.objects.filter(Q(nombres__icontains=q) | Q(apellido_pat__icontains=q) | Q(apellido_mat__icontains=q) | Q(nro_documento__istartswith=q))
        qs = self.get_results(qs)        
        return JsonResponse({
            'results': qs
        }, content_type='application/json')

    def get_results(self, results):
        return [dict(id=x.id, text=x.nombres+' '+x.apellido_pat+' '+x.apellido_mat+' - '+x.nro_documento) for x in results]

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