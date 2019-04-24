from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import IndexView, PersonaRegistrar, PersonaEditar


urlpatterns = [
    path('', login_required(IndexView.as_view()), name='persona-index'),
    path('registrar', login_required(PersonaRegistrar.as_view()), name='persona_registrar'),
    path('<pk>/editar', login_required(PersonaEditar.as_view()), name='persona-editar'),
]