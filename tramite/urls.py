from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import IndexView, TramiteRegistrar, TramiteEditar, PersonaAutocomplete, CreateTramitePersona, CreateTramiteViaje, DeleteTramitePersona, DeleteTramiteViaje, ReportTramitePdf, ReporteViajePdf, TramiteEliminar, TableAsJSON


urlpatterns = [
    path('', login_required(IndexView.as_view()), name='tramite-index'),
    url(r'^persona-autocomplete/$', login_required(PersonaAutocomplete.as_view()), name='persona_autocomplete'),
    url(r'^as_json/$',login_required(TableAsJSON.as_view()), name='table-as-json'),
    path('registrar', login_required(TramiteRegistrar.as_view()), name='tramite-registrar'),
    path('<pk>/editar', login_required(TramiteEditar.as_view()), name='tramite-editar'),
    path('<pk>/eliminar', login_required(TramiteEliminar.as_view()), name='tramite_eliminar'),
    path('tramitepersona/registrar', login_required(CreateTramitePersona.as_view()), name='tramitepersona-registrar'),
    path('tramiteviaje/registrar', login_required(CreateTramiteViaje.as_view()), name='tramiteviaje-registrar'),
    path('tramitepersona/eliminarajax/<pk>', login_required(DeleteTramitePersona.as_view()), name='tramitepersona_eliminar'),
    path('tramiteviaje/eliminarajax/<pk>', login_required(DeleteTramiteViaje.as_view()), name='tramiteviaje_eliminar'),
    path('<int:id>/reporte_pdf', login_required(ReportTramitePdf.as_view()), name='reporte_tramite'),
    path('<int:id>/reporteviaje_pdf', login_required(ReporteViajePdf.as_view()), name='reporte_viaje')
]