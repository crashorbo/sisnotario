from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from django.db.models.query import QuerySet

class MyModelMixin(object):

  def q_for_search_word(self, word):
    return Q(nombres__icontains=word) | Q(apellido_pat__icontains=word)| Q(apellido_mat__icontains=word) | Q(nro_documento__icontains=word) | Q(expedido__icontains=word)

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

class Persona(models.Model):

  GENERO_CHOICES = (
    (1, 'MASCULINO'),
    (2, 'FEMENINO'),
  )

  EXPEDIDO_CHOICES = (
    (0, ''),
    (1, 'ORURO'),
    (2, 'LA PAZ'),
    (3, 'COCHABAMBA'),
    (4, 'SANTA CRUZ'),
    (5, 'CHUQUISACA'),
    (6, 'POTOSI'),
    (7, 'TARIJA'),
    (8, 'BENI'),
    (9, 'PANDO'),
  )

  EXPEDIDO_PRINT = {
    0: '',
    1: 'ORURO',
    2: 'LA PAZ',
    3: 'COCHABAMBA',
    4: 'SANTA CRUZ',
    5: 'CHUQUISACA',
    6: 'POTOSI',
    7: 'TARIJA',
    8: 'BENI',
    9: 'PANDO',
  }

  ESTADO_CIVIL = (
    (1, 'SOLTERO(A)'),
    (2, 'CASADO(A)'),
    (3, 'VIUDO(A)'),
    (4, 'DIVORCIADO(A)'),
  )
  TIPO_PERSONA = (
    (0, 'NATURAL'),
    (1, 'JURIDICO(A)'),
  )
  nombres = models.CharField(max_length=100)
  apellido_pat = models.CharField(max_length=100, blank=True)
  apellido_mat = models.CharField(max_length=100, blank=True)
  expedido = models.IntegerField(default=0, choices=EXPEDIDO_CHOICES)
  nro_documento = models.CharField(max_length=50, unique=True)
  estado_civil = models.IntegerField(default=1, choices=ESTADO_CIVIL)
  genero = models.IntegerField(default=1, choices=GENERO_CHOICES)
  nacionalidad = models.CharField(max_length=100, default="BOLIVIANA")
  telefono = models.CharField(max_length=50, default='', blank=True)
  email = models.EmailField(max_length=200, blank=True)
  fecha_nacimiento = models.DateField(default=timezone.now)
  direccion = models.CharField(max_length=200, blank=True)
  tipo_persona = models.IntegerField(default=0, choices=TIPO_PERSONA)
  natural = models.CharField(max_length=200, default='', blank=True)
  fecha_registro = models.DateTimeField(default=timezone.now)
  fecha_actualizacion = models.DateTimeField(default=timezone.now)
  razon_social = models.CharField(max_length=200, default='', blank=True)
  poder = models.CharField(max_length=200, default='', blank=True)
  nit = models.CharField(max_length=20, default='', blank=True)
  fundempresa = models.CharField(max_length=20, default='', blank=True)

  objects = MyModelManager()

  def __str__(self):
    return self.nombres + ' ' + self.apellido_pat + ' ' +self.apellido_mat + ' - ' + self.nro_documento

  def as_list(self):
    return [self.nombres + ' ' + self.apellido_pat + ' ' +self.apellido_mat,
      self.nro_documento,
      self.EXPEDIDO_PRINT[self.expedido],
      self.telefono,
      '<button data-url="/persona/'+str(self.id)+'/editar" class="btn editar-persona btn-simple btn-warning btn-xs"><i class="fa fa-edit"></i></button>'
      ]


class Personaback(models.Model):

  GENERO_CHOICES = (
    (1, 'MASCULINO'),
    (2, 'FEMENINO'),
  )

  EXPEDIDO_CHOICES = (
    (1, 'ORURO'),
    (2, 'LA PAZ'),
    (3, 'COCHABAMBA'),
    (4, 'SANTA CRUZ'),
    (5, 'CHUQUISACA'),
    (6, 'POTOSI'),
    (7, 'TARIJA'),
    (8, 'BENI'),
    (9, 'PANDO'),
  )

  ESTADO_CIVIL = (
    (1, 'SOLTERO(A)'),
    (2, 'CASADO(A)'),
    (3, 'VIUDO(A)'),
    (4, 'DIVORCIADO(A)'),
  )
  TIPO_PERSONA = (
    (0, 'NATURAL'),
    (1, 'JURIDICO(A)'),
  )
  codigo = models.IntegerField(default=0)
  nombres = models.CharField(max_length=100)
  apellido_pat = models.CharField(max_length=100, blank=True)
  apellido_mat = models.CharField(max_length=100, blank=True)
  expedido = models.IntegerField(default=1, choices=EXPEDIDO_CHOICES)
  nro_documento = models.CharField(max_length=50, unique=True)
  estado_civil = models.IntegerField(default=1, choices=ESTADO_CIVIL)
  genero = models.IntegerField(default=1, choices=GENERO_CHOICES)
  nacionalidad = models.CharField(max_length=100, default="BOLIVIANA")
  telefono = models.CharField(max_length=50, default='', blank=True)
  email = models.EmailField(max_length=200, blank=True)
  fecha_nacimiento = models.DateField(default=timezone.now)
  direccion = models.CharField(max_length=200, blank=True)
  tipo_persona = models.IntegerField(default=0, choices=TIPO_PERSONA)
  natural = models.CharField(max_length=200, default='', blank=True)
  fecha_registro = models.DateTimeField(default=timezone.now)
  fecha_actualizacion = models.DateTimeField(default=timezone.now)
  razon_social = models.CharField(max_length=200, default='', blank=True)
  poder = models.CharField(max_length=200, default='', blank=True)
  nit = models.CharField(max_length=20, default='', blank=True)
  fundempresa = models.CharField(max_length=20, default='', blank=True)

  def __str__(self):
    return self.nombres + ' ' + self.apellido_pat + ' ' +self.apellido_mat + ' - ' + self.nro_documento