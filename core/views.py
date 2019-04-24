from django.shortcuts import render
from django.views.generic import TemplateView, View
# Create your views here.


# Vista Inicial de la aplicacion
class IndexView(TemplateView):
    template_name = 'core/index.html'