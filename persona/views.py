from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import View
from django.db.models import Q
from django.http import JsonResponse
from braces.views import JSONResponseMixin
from .models import Persona
from .forms import PersonaForm
# Create your views here.

class TableAsJSON(JSONResponseMixin, View):
  model = Persona

  def get(self, request, *args, **kwargs):
    col_name_map = {
      '0': 'nombres',
      '1': 'nro_documento',
      '2': 'expedido',
      '3': 'telefono',
      '4': '',
    }
    object_list = self.model.objects.all()
    search_text = request.GET.get('sSearch', '').lower()
    start = int(request.GET.get('iDisplayStart', 0))
    delta = int(request.GET.get('iDisplayLength', 50))
    sort_dir = request.GET.get('sSortDir_0', 'asc')
    sort_col = int(request.GET.get('iSortCol_0', 0))
    sort_col_name = request.GET.get('mDataProp_%s' % sort_col, '1')
    sort_dir_prefix = (sort_dir == 'desc' and '-' or '')

    if sort_col_name in col_name_map:
      sort_col = col_name_map[sort_col_name]
      object_list = object_list.order_by('%s%s' % (sort_dir_prefix, sort_col))

    filtered_object_list = object_list
    if len(search_text) > 0:
      filtered_object_list = object_list.filter_on_search(search_text)

    json = {
      "iTotalRecords": object_list.count(),
      "iTotalDisplayRecords": filtered_object_list.count(),
      "sEcho": request.GET.get('sEcho', 1),
      "aaData": [obj.as_list() for obj in filtered_object_list[start:(start+delta)]]
    }
    return self.render_json_response(json)

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

class PersonaVerificar(View):
    def get(self, *args, **kwargs):
        n = self.request.GET['n']
        e = self.request.GET['e']
        try:
            persona = Persona.objects.get(nro_documento=n, expedido=e)
            return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False})