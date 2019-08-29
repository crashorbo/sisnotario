import csv
from django.contrib.auth.models import User
from tramite.models import Tramiteback, Tramitepersonaback, Tramite, Tramitepersona
from persona.models import Personaback, Persona

def migrarTramites():
    with open('csvpath/tramitebackf.csv') as csvfile:
        rowreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in rowreader:
            tramite = Tramiteback()
            tramite.codigo = row[0]
            tramite.tipo_tramite = row[1]
            tramite.numero = row[2]
            tramite.gestion = row[3]
            tramite.titulo = row[4]
            tramite.fecha_documento = row[5]
            tramite.fecha_registro = row[6]
            tramite.hora_registro = row[7]
            tramite.fecha_actualizacion = row[8]
            tramite.formularios = row[9]
            tramite.parte = row[10]
            tramite.parte_imp = row[11]
            tramite.parte_aux = row[12]
            tramite.contra_parte = row[13]
            tramite.contra_parte_imp = row[14]
            if row[15] == 't':
                tramite.estado = True
            else:
                tramite.estado = False
            
            tramite.save()

def migrarTramitePersona():
    with open('csvpath/tramitepersonabackf.csv') as csvfile:
        rowreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in rowreader:
            tramite = Tramitepersonaback()
            tramite.codigo = row[0]
            if row[1] == 't':
                tramite.firma = True
            else:
                tramite.firma = False
            if row[2] == 't':
                tramite.testigo = True
            else:
                tramite.testigo = False
            tramite.tipo = row[3]
            if row[4] == 't':
                tramite.contra_parte = True
            else:
                tramite.contra_parte = False    
            tramite.persona = row[5]
            tramite.tramite = row[6]
            tramite.save()

def migrarPersona():
    with open('csvpath/personabackf.csv') as csvfile:
        rowreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in rowreader:
            print(row[0])
            persona = Personaback()
            persona.codigo = row[0]
            persona.nombres = row[1]
            persona.apellido_pat = row[2]
            persona.apellido_mat = row[3]
            persona.expedido = row[4]
            persona.nro_documento = row[5]
            persona.estado_civil = row[6]
            persona.genero = row[7]
            persona.nacionalidad = row[8]
            persona.telefono = row[9]
            persona.email = row[10]
            persona.fecha_nacimiento = row[11]
            persona.direccion = row[12]
            persona.tipo_persona = row[13]
            persona.natural = row[14]
            persona.fecha_registro = row[15]
            persona.fecha_actualizacion = row[16]
            persona.razon_social = row[17]
            persona.poder = row[18]
            persona.nit = row[19]
            persona.fundempresa = row[20]
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
            formularios=aux.formularios, parte=aux.parte, parte_imp=aux.parte_imp, parte_aux=aux.parte_aux, contra_parte=aux.contra_parte, 
            contra_parte_imp=aux.contra_parte_imp, estado=aux.estado, )
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
                tramite_persona = Tramitepersona(tramite=tramite, persona=persona, firma=tp.firma, testigo=tp.testigo, tipo=tp.tipo, contra_parte=tp.contra_parte)
                tramite_persona.save()
                print(persona_back.codigo)