from django import forms
from .models import Persona

class PersonaForm(forms.ModelForm):
  class Meta:
    model = Persona
    fields = {
      'nombres', 'apellido_pat', 'apellido_mat', 'expedido', 'nro_documento', 'estado_civil',
      'genero', 'nacionalidad', 'fecha_nacimiento', 'direccion', 'natural',
      'tipo_persona', 'razon_social', 'nit', 'poder', 'fundempresa', 'telefono',
      'email'
    }
    widgets = {
      'nombres': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
      'apellido_pat': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
      'apellido_mat': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
      'expedido': forms.Select(attrs={'class': 'form-control form-control-sm'}),
      'nro_documento': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
      'estado_civil': forms.Select(attrs={'class': 'form-control form-control-sm'}),
      'genero': forms.Select(attrs={'class': 'form-control form-control-sm'}),
      'nacionalidad': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
      'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control fecha form-control-sm'}),
      'direccion': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 2}),
      'natural': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
      'tipo_persona': forms.Select(attrs={'class': 'form-control form-control-sm'}),
      'razon_social': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
      'nit': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
      'poder': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
      'fundempresa': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
      'telefono': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
      'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm'}),
    }