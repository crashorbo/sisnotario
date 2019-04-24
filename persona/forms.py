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
      'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NOMBRES'}),
      'apellido_pat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'APELLIDO PATERNO'}),
      'apellido_mat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'APELLIDO MATERNA'}),
      'expedido': forms.Select(attrs={'class': 'form-control', 'placeholder': 'EXPEDIDO'}),
      'nro_documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NUMERO DOCUMENTO'}),
      'estado_civil': forms.Select(attrs={'class': 'form-control', 'placeholder': 'ESTADO CIVIL'}),
      'genero': forms.Select(attrs={'class': 'form-control', 'placeholder': 'GENERO'}),
      'nacionalidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NACIONALIDAD'}),
      'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control fecha', 'placeholder': 'FECHA NACIMIENTO'}),
      'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3 , 'placeholder': 'DIRECCION'}),
      'natural': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NATURAL DE'}),
      'tipo_persona': forms.Select(attrs={'class': 'form-control', 'placeholder': 'TIPO PERSONA'}),
      'razon_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RAZON SOCIAL'}),
      'nit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NIT'}),
      'poder': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PODER'}),
      'fundempresa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'FUNDEMPRESA'}),
      'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'TELEFONO'}),
      'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'CORREO ELECTRONICO'}),
    }