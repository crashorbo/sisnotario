from django.db import models
from django.conf import settings
import datetime
from django.db.models import Q
from django.db.models.query import QuerySet

from django.contrib.auth.models import User
from persona.models import Persona

class MyModelMixin(object):

  def q_for_search_word(self, word):
    return Q(numero__icontains=word) | Q(fecha_registro__icontains=word)| Q(parte__icontains=word) | Q(contra_parte__icontains=word) | Q(titulo__icontains=word)

  def q_for_search(self, search):
    q = Q()
    if search:
        searches = search.split()
        for word in searches:
            q = q & self.q_for_search_word(word)
    return q

  def filter_on_search(self, search):
    return self.filter(self.q_for_search(search))

class MyModelQuerySet(QuerySet, MyModelMixin):
  pass

class MyModelManager(models.Manager, MyModelMixin):
  
  def get_queryset(self):
    return MyModelQuerySet(self.model, using=self._db)

class Tramite(models.Model):
  TIPO_TRAMITE = (
    (1, 'CERTIFICACION FIRMAS Y RUBRICAS'),
  )

  TIPO_TRAMITE_PRINT = {
    1: 'CERTIFICACION FIRMAS Y RUBRICAS',
    2: 'AUTORIZACION DE VIAJE DE MENOR',
  }

  usuario = models.ForeignKey(User, on_delete=models.CASCADE)
  tipo_tramite = models.IntegerField(choices=TIPO_TRAMITE, default=1, blank=False)
  numero = models.IntegerField(default=0)
  gestion = models.IntegerField(default=0)
  titulo = models.CharField(blank=True, max_length=250)
  fecha_documento = models.DateField(default=datetime.datetime.now)
  fecha_registro = models.DateField(default=datetime.datetime.now)
  hora_registro = models.TimeField(default=datetime.datetime.now)
  fecha_actualizacion = models.DateTimeField(auto_now=True)
  formularios = models.CharField(blank=True, max_length=250)
  parte = models.TextField(blank=True)
  parte_imp = models.CharField(blank=True, max_length=200)
  parte_aux = models.CharField(blank=True, max_length=200)
  contra_parte = models.TextField(blank=True)
  contra_parte_imp = models.CharField(blank=True, max_length=200)
  estado = models.BooleanField(default=False)

  objects = MyModelManager()

  def __str__(self):
    return str(self.numero)

  def as_list(self):
    return [self.numero,
      self.fecha_registro.strftime("%d/%m/%Y"),
      self.TIPO_TRAMITE_PRINT[self.tipo_tramite],
      '<span class="label '+self.estadoclass()+'">'+self.estadotext()+'</span>',
      self.titulo,
      self.parte,
      self.contra_parte,
      '<a href="/tramite/'+str(self.id)+'/editar" data-toggle="tooltip" data-original-title="Editar"><i class="fa fa-pencil text-inverse m-r-10"></i></a>',
      ]

  def estadoclass(self):
    if(self.estado):
      return 'label-success'
    else:
      return 'label-danger'

  def estadotext(self):
    if(self.estado):
      return 'TERMINADO'
    else:
      return 'TRANSITO'  

class Tramitepersona(models.Model):
  tramite = models.ForeignKey(Tramite, on_delete=models.CASCADE)
  persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
  firma = models.BooleanField(default=True)
  testigo = models.BooleanField(default=False)
  tipo = models.IntegerField(default=0)
  contra_parte = models.BooleanField(default=True)
  class Meta:
    ordering = ('id', )

  def __str__(self):
    return self.id

class Tramiteviaje(models.Model):
  tramite = models.ForeignKey(Tramite, on_delete=models.CASCADE)
  persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
  certificado_nacimiento = models.CharField(blank=True, max_length=50)
  destino = models.CharField(blank=True, max_length=250)
  motivo_viaje = models.CharField(blank=True, max_length=250)
  residencia_viaje = models.CharField(blank=True, max_length=250)
  tiempo_ausencia = models.IntegerField(default=0)
  fecha_retorno = models.DateField(default=datetime.datetime.now)
  objeto_viaje = models.CharField(blank=True, max_length=250)
  acompanante = models.BooleanField(default=False)
  tipo = models.BooleanField(default=False)
  firma = models.BooleanField(default=True)
  lugar_trabajo = models.CharField(blank=True, max_length=200)

  def __str__(self):
    return self.id

class Numerotramite(models.Model):
  numero = models.IntegerField()
  gestion = models.IntegerField()
  tipo = models.IntegerField()


class Tramiteback(models.Model):
  TIPO_TRAMITE = (
    (1, 'CERTIFICACION FIRMAS Y RUBRICAS'),
    (2, 'AUTORIZACION DE VIAJE DE MENOR'),
  )

  TIPO_TRAMITE_PRINT = {
    1: 'CERTIFICACION FIRMAS Y RUBRICAS',
    2: 'AUTORIZACION DE VIAJE DE MENOR',
  }

  codigo = models.IntegerField(default=0)
  tipo_tramite = models.IntegerField(choices=TIPO_TRAMITE, default=1, blank=False)
  numero = models.IntegerField(default=0)
  gestion = models.IntegerField(default=0)
  titulo = models.CharField(blank=True, max_length=250)
  fecha_documento = models.DateField(default=datetime.datetime.now)
  fecha_registro = models.DateField(default=datetime.datetime.now)
  hora_registro = models.TimeField(default=datetime.datetime.now)
  fecha_actualizacion = models.DateTimeField(auto_now=True)
  formularios = models.CharField(blank=True, max_length=250)
  parte = models.TextField(blank=True)
  parte_imp = models.CharField(blank=True, max_length=200)
  parte_aux = models.CharField(blank=True, max_length=200)
  contra_parte = models.TextField(blank=True)
  contra_parte_imp = models.CharField(blank=True, max_length=200)
  estado = models.BooleanField(default=False)

class Tramitepersonaback(models.Model):
  codigo = models.IntegerField(default=0)
  tramite = models.IntegerField(default=0)
  persona = models.IntegerField(default=0)
  firma = models.BooleanField(default=True)
  testigo = models.BooleanField(default=False)
  tipo = models.IntegerField(default=0)
  contra_parte = models.BooleanField(default=True)
  class Meta:
    ordering = ('id', )

  def __str__(self):
    return self.id