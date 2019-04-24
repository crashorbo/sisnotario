from django import template

register = template.Library()

@register.filter(name='concatstring')
def concatstring(arg1, arg2):  
  return str(arg1) + str(arg2)

@register.filter(name='tipo_tramite')
def tipo(value):
  TRAMITE_CHOICE = {
    1: 'CERTIFICACION FIRMAS Y RUBRICAS',
    2: 'AUTORIZACION DE VIAJE DE MENOR',
  }
  return TRAMITE_CHOICE[value]

@register.filter(name='estado_tramite')
def estado(value):
  ESTADO_CHOICE = {
    0: 'TRANSITO',
    1: 'TERMINADO',
  }
  return ESTADO_CHOICE[value]

@register.filter(name='firma')
def firma(value):
  ESTADO_CHOICE = {
    0: 'NO',
    1: 'SI',
  }
  return ESTADO_CHOICE[value]

@register.filter(name='expedido')
def expedido(value):
  EXPEDIDO_CHOICE = {
    1: 'OR',
    2: 'LP',
    3: 'CB',
    4: 'SC',
    5: 'CH',
    6: 'PT',
    7: 'TJ',
    8: 'BN',
    9: 'PA',
  }
  return EXPEDIDO_CHOICE[value]

@register.filter(name='fechaupper')
def fechaupper(value):
  FECHA_CHOICE = {
    1: 'ENERO',
    2: 'FEBRERO',
    3: 'MARZO',
    4: 'ABRIL',
    5: 'MAYO',
    6: 'JUNIO',
    7: 'JULIO',
    8: 'AGOSTO',
    9: 'SEPTIEMBRE',
    10: 'OCTUBRE',
    11: 'NOVIEMBRE',
    12: 'DICIEMBRE',
  }
  return str(value.day)+' DE '+FECHA_CHOICE[value.month]+' DE '+str(value.year)

@register.filter(name='mesupper')
def mesupper(value):
  MES_CHOICE = {
    1: 'ENERO',
    2: 'FEBRERO',
    3: 'MARZO',
    4: 'ABRIL',
    5: 'MAYO',
    6: 'JUNIO',
    7: 'JULIO',
    8: 'AGOSTO',
    9: 'SEPTIEMBRE',
    10: 'OCTUBRE',
    11: 'NOVIEMBRE',
    12: 'DICIEMBRE',
  }
  return MES_CHOICE[value]

@register.filter(name='diaupper')
def diaupper(value):
  DIA_CHOICE = {
    'Sunday': 'DOMINGO',
    'Monday': 'LUNES',
    'Tuesday': 'MARTES',
    'Wednesday': 'MIERCOLES',
    'Thursday': 'JUEVES',
    'Friday': 'VIERNES',
    'Saturday': 'SABADO'
  }
  return DIA_CHOICE[value]

@register.filter(name='horareg')
def horareg(value):
  hora = str(value.hour)
  if len(hora) < 2:
    hora = '0'+hora
  minutos = str(value.minute)
  if len(minutos) < 2:
    minutos = '0'+minutos
  segundos = str(value.second)
  if len(segundos) < 2:
    segundos = '0'+segundos
  return hora+':'+minutos+':'+segundos

def titulouno(value):
  if len(value) > 59:
    return value[0:58]
  return value

def titulodos(value):
  if len(value) <= 59:
    return ''
  if len(value) > 108:
    return value[58:108]
  return value[58:len(value)-1]

def tramitantes(fi,nf,te):
  resultado = []
  i = 0
  j = 0
  k = 0
  while ((i < len(fi)) or (j < len(nf)) or (k < len(te))):
    l = 0
    fir = []
    nfr = []
    tes = []
    while l < 4:
      if i < len(fi):
        fir.append(fi[i])
      else:
        fir.append(None)  
      l = l + 1
      i = i + 1
    l = 0
    while l < 2:
      if j < len(nf):
        nfr.append(nf[j])
      else:
        nfr.append(None)
      l = l + 1
      j = j + 1  
    l = 0
    while l < 2:
      if k < len(te):
        tes.append(te[k])
      else:
        tes.append(None)
      l = l + 1
      k = k + 1  
    resaux = [fir, nfr, tes]
    resultado.append(resaux)
  return resultado
  

  