from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import IndexView, PersonaRegistrar, PersonaEditar, PersonaAutocomplete


urlpatterns = [
    path('', login_required(IndexView.as_view()), name='persona-index'),
    path('registrar', login_required(PersonaRegistrar.as_view()), name='persona_registrar'),
    path('<pk>/editar', login_required(PersonaEditar.as_view()), name='persona-editar'),
    url(r'^persona-autocomplete/$', login_required(PersonaAutocomplete.as_view()), name='persona-autocomplete'),
]