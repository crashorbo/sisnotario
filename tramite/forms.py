from django import forms
from dal import autocomplete
from .models import Tramite, Tramitepersona, Tramiteviaje
from persona.models import Persona

class TramiteForm(forms.ModelForm):
    class Meta:
        model = Tramite
        fields = {
            'tipo_tramite', 'titulo', 'formularios', 'fecha_documento', 'hora_registro', 'parte_aux'
        }
        widgets = {
            'tipo_tramite': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'titulo': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 2}),
            'formularios':  forms.TextInput(attrs={'class': 'form-control form-control-sm', 'data-role':'tagsinput'}),
            'fecha_documento': forms.DateInput(attrs={'class': 'form-control form-control-sm fecha'}),
            'hora_registro': forms.TimeInput(attrs={'class': 'form-control form-control-sm'}),
            'parte_aux': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }

class TramitePersonaForm(forms.ModelForm):
    persona = forms.ModelChoiceField(queryset=Persona.objects.all(), empty_label="Seleccionar Persona", widget=autocomplete.ModelSelect2(url='persona-autocomplete', attrs={'class': 'form-control form-control-sm'}))
    class Meta:
        model = Tramitepersona
        fields = {
            'persona', 'tramite', 'firma', 'testigo', 'contra_parte'
        }
        widgets = {
            'tramite': forms.TextInput(attrs={'class': 'form-control'}),
            'firma': forms.CheckboxInput(attrs={'class': 'filled-in chk-col-orange'}),
            'testigo': forms.CheckboxInput(attrs={'class': 'filled-in chk-col-indigo'}),
            'contra_parte': forms.CheckboxInput(attrs={'class': 'filled-in chk-col-indigo'}),
        }

class TramiteViajeForm(forms.ModelForm):
    persona = forms.ModelChoiceField(queryset=Persona.objects.all(), empty_label="Seleccionar Persona", widget=autocomplete.ModelSelect2(url='persona-autocomplete', attrs={'class': 'form-control form-control-sm'}))
    class Meta:
        model = Tramiteviaje
        fields = {
            'persona', 'tramite', 'certificado_nacimiento', 'destino', 'motivo_viaje', 'residencia_viaje', 'tiempo_ausencia', 'fecha_retorno', 'objeto_viaje', 'tipo', 'acompanante','firma','lugar_trabajo'
        }
        widgets = {
            'tramite': forms.TextInput(attrs={'class': 'form-control'}),
            'certificado_nacimiento': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),    
            'destino': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'motivo_viaje': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'lugar_trabajo': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'residencia_viaje': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'tiempo_ausencia': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'fecha_retorno': forms.DateInput(attrs={'class': 'form-control form-control-sm fecha'}),
            'objeto_viaje': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'firma': forms.CheckboxInput(attrs={'class': 'filled-in chk-col-orange form-control-sm'}),
            'tipo': forms.CheckboxInput(attrs={'class': 'filled-in chk-col-orange form-control-sm'}),
            'acompanante': forms.CheckboxInput(attrs={'class': 'filled-in chk-col-purple form-control-sm'}),
        }