from django import forms
from .models import Tramite, Tramitepersona, Tramiteviaje
from persona.models import Persona

class TramiteForm(forms.ModelForm):
    class Meta:
        model = Tramite
        fields = {
            'tipo_tramite', 'titulo', 'pagina_inicio', 'pagina_fin', 'fecha_documento', 'hora_registro'
        }
        widgets = {
            'tipo_tramite': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'pagina_inicio':  forms.NumberInput(attrs={'class': 'form-control'}),
            'pagina_fin':  forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_documento': forms.DateInput(attrs={'class': 'form-control fecha', 'placeholder': 'FECHA DOCUMENTO'}),
            'hora_registro': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'HORA DOCUMENTO'}),
        }

class TramitePersonaForm(forms.ModelForm):
    persona = forms.ModelChoiceField(queryset=Persona.objects.all(), empty_label="Seleccionar Persona", widget=forms.Select(attrs={'class': 'form-control select2'}))
    class Meta:
        model = Tramitepersona
        fields = {
            'persona', 'tramite', 'firma', 'testigo'
        }
        widgets = {
            'tramite': forms.TextInput(attrs={'class': 'form-control'}),
            'firma': forms.CheckboxInput(attrs={'class': 'filled-in chk-col-orange'}),
            'testigo': forms.CheckboxInput(attrs={'class': 'filled-in chk-col-indigo'})
        }

class TramiteViajeForm(forms.ModelForm):
    persona = forms.ModelChoiceField(queryset=Persona.objects.all(), empty_label="Seleccionar Persona", widget=forms.Select(attrs={'class': 'form-control select2'}))
    class Meta:
        model = Tramiteviaje
        fields = {
            'persona', 'tramite', 'certificado_nacimiento', 'destino', 'motivo_viaje', 'residencia_viaje', 'tiempo_ausencia', 'fecha_retorno', 'objeto_viaje', 'tipo'
        }
        widgets = {
            'tramite': forms.TextInput(attrs={'class': 'form-control'}),
            'certificaco_nacimiento': forms.TextInput(attrs={'class': 'form-control'}),    
            'destino': forms.TextInput(attrs={'class': 'form-control'}),
            'motivo_viaje': forms.TextInput(attrs={'class': 'form-control'}),
            'residencia_viaje': forms.TextInput(attrs={'class': 'form-control'}),
            'tiempo_ausencia': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_retorno': forms.DateInput(attrs={'class': 'form-control'}),
            'objeto_viaje': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.CheckboxInput(attrs={'class': 'filled-in chk-col-orange'}),
        }