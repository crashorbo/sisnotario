import csv
from django.contrib.auth.models import User
from tramite.models import Tramiteback, Tramitepersonaback, Tramite, Tramitepersona
from persona.models import Personaback, Persona

def migrarTramites():
    with open('csvpath/tramitesback.csv') as csvfile:
        rowreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in rowreader:
            tramite = Tramiteback()
            tramite.codigo = row[0]
            tramite.tipo_tramite = row[1]
            tramite.numero = row[2]
            tramite.titulo = row[3]
            tramite.formularios = row[5]
            tramite.fecha_registro = row[6]
            tramite.hora_registro = row[7]
            tramite.fecha_actualizacion = row[8]
            if row[9] == 't':
                tramite.estado = True
            else:
                tramite.estado = False
            tramite.gestion = row[13]
            tramite.fecha_documento = row[14]
            tramite.save()

def migrarTramitePersona():
    with open('csvpath/tramitepersonaback.csv') as csvfile:
        rowreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in rowreader:
            tramite = Tramitepersonaback()
            tramite.codigo = row[0]
            if row[1] == 't':
                tramite.firma = True
            else:
                tramite.firma = False
            tramite.tipo = row[2]
            tramite.persona = row[3]
            tramite.tramite = row[4]
            if row[5] == 't':
                tramite.testigo = True
            else:
                tramite.testigo = False
            tramite.save()

def migrarPersona():
    with open('csvpath/personaback.csv') as csvfile:
        rowreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in rowreader:
            print(row[0])
            persona = Personaback()
            persona.codigo = row[0]
            persona.nombres = row[1]
            persona.expedido = row[2]
            persona.nro_documento = row[3]
            persona.estado_civil = row[4]
            persona.genero = row[5]
            persona.nacionalidad = row[6]
            persona.fecha_nacimiento = row[7]
            persona.direccion = row[8]
            persona.fecha_registro = row[9]
            persona.fecha_actualizacion = row[10]
            persona.natural = row[11]
            persona.tipo_persona = row[12]
            persona.fundempresa = row[13]
            persona.nit = row[14]
            persona.poder = row[15]
            persona.razon_social = row[16]
            persona.email = row[17]
            persona.telefono = row[18]
            persona.apellido_mat = row[19]
            persona.apellido_pat = row[20]
            persona.save()

def migrarBackup():
    tramites_back = Tramiteback.objects.all()
    usuario = User.objects.get(id=1)
    for aux in tramites_back:
        try:
            tb = Tramite.objects.get(numero = aux.numero)
            print('tramite ya existe')
        except:
            tramitepersonas_back = Tramitepersonaback.objects.filter(tramite=aux.codigo)
            tramite = Tramite(usuario=usuario, tipo_tramite=aux.tipo_tramite, numero=aux.numero, gestion=aux.gestion, titulo=aux.titulo,
            fecha_documento=aux.fecha_documento, fecha_registro=aux.fecha_registro, hora_registro=aux.hora_registro, fecha_actualizacion=aux.fecha_actualizacion, 
            formularios=aux.formularios, estado=aux.estado)
            tramite.save()
            print(aux.codigo)
            for tp in tramitepersonas_back:
                persona_back = Personaback.objects.get(codigo=tp.persona)
                try:
                    persona = Persona.objects.get(nro_documento=persona_back.nro_documento, expedido=persona_back.expedido)
                    print(persona.id, 'existe')
                except:
                    persona = Persona(nombres=persona_back.nombres, apellido_pat=persona_back.apellido_pat, apellido_mat=persona_back.apellido_mat,
                    expedido=persona_back.expedido, nro_documento=persona_back.nro_documento, estado_civil=persona_back.estado_civil,
                    genero=persona_back.genero, nacionalidad=persona_back.nacionalidad, telefono=persona_back.telefono, email=persona_back.email,
                    fecha_nacimiento=persona_back.fecha_nacimiento, direccion=persona_back.direccion, tipo_persona=persona_back.tipo_persona,
                    natural=persona_back.natural, fecha_registro=persona_back.fecha_registro, fecha_actualizacion=persona_back.fecha_actualizacion,
                    razon_social=persona_back.razon_social, poder=persona_back.poder, nit=persona_back.nit, fundempresa=persona_back.fundempresa)
                    persona.save()
                    print(persona.id, 'guardado')
                    tramite_persona = Tramitepersona(tramite=tramite, persona=persona, firma=tp.firma, testigo=tp.testigo, tipo=tp.tipo)
                    tramite_persona.save()
                    print(persona_back.codigo)
        break