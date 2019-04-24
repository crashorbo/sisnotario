from django.db import models
from django.utils import timezone
from django.conf import settings

class Persona(models.Model):

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
  nombres = models.CharField(max_length=100)
  apellido_pat = models.CharField(max_length=100, blank=True)
  apellido_mat = models.CharField(max_length=100, blank=True)
  expedido = models.IntegerField(default=1, choices=EXPEDIDO_CHOICES)
  nro_documento = models.CharField(max_length=50, unique=True)
  estado_civil = models.IntegerField(default=1, choices=ESTADO_CIVIL)
  genero = models.IntegerField(default=1, choices=GENERO_CHOICES)
  nacionalidad = models.CharField(max_length=100)
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