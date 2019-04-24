from django.db import models
from django.conf import settings
from datetime import datetime, date, time

from django.contrib.auth.models import User
from persona.models import Persona

class Tramite(models.Model):
  TIPO_TRAMITE = (
    (1, 'CERTIFICACION FIRMAS Y RUBRICAS'),
    (2, 'AUTORIZACION DE VIAJE DE MENOR'),
  )

  usuario = models.ForeignKey(User, on_delete=models.SET_NULL, blank = True,null=True)
  tipo_tramite = models.IntegerField(choices=TIPO_TRAMITE, default=1, blank=False)
  numero = models.IntegerField(default=0)
  gestion = models.IntegerField(default=0)
  titulo = models.CharField(blank=True, max_length=250)
  titulo_aux = models.CharField(blank=True, max_length=250)
  formularios = models.CharField(blank=True, max_length=100)
  fecha_documento = models.DateField(default=datetime.now)
  fecha_registro = models.DateField(default=datetime.now)
  hora_registro = models.TimeField(default=datetime.now)
  fecha_actualizacion = models.DateTimeField(auto_now=True)
  pagina_inicio = models.IntegerField(default=0, blank=True)
  pagina_fin = models.IntegerField(default=0, blank=True)
  estado = models.BooleanField(default=False)
  
  def __str__(self):
      return str(self.numero)

class Tramitepersona(models.Model):
  tramite = models.ForeignKey(Tramite, on_delete=models.CASCADE)
  persona = models.ForeignKey(Persona, on_delete=models.SET_NULL, blank=True, null=True)
  firma = models.BooleanField(default=True)
  testigo = models.BooleanField(default=False)
  tipo = models.IntegerField(default=0)
  
  class Meta:
    ordering = ('id',)

  def __str__(self):
    return self.id

class Tramiteviaje(models.Model):
  tramite = models.ForeignKey(Tramite, on_delete=models.CASCADE)
  persona = models.ForeignKey(Persona, on_delete=models.SET_NULL, blank=True, null=True)
  certificado_nacimiento = models.CharField(blank=True, max_length=50)
  destino = models.CharField(blank=True, max_length=250)
  motivo_viaje = models.CharField(blank=True, max_length=250)
  residencia_viaje = models.CharField(blank=True, max_length=250)
  tiempo_ausencia = models.IntegerField(default=0)
  fecha_retorno = models.DateField(default=datetime.now)
  objeto_viaje = models.CharField(blank=True, max_length=250)
  tipo = models.BooleanField(default=False)

  def __str__(self):
    return self.id

class Numerotramite(models.Model):
  numero = models.IntegerField()
  gestion = models.IntegerField()
  tipo = models.IntegerField()