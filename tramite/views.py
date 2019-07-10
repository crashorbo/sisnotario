from django.shortcuts import render, HttpResponse
from django.views.generic.list import ListView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, date, time
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import legal
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing 
from reportlab.graphics.barcode.qr import QrCodeWidget 
from reportlab.graphics import renderPDF

from braces.views import JSONResponseMixin
from django.contrib.auth.models import User
from .models import Tramite, Tramitepersona, Numerotramite, Tramiteviaje
from persona.models import Persona
from .forms import TramiteForm, TramitePersonaForm, TramiteViajeForm
from .templatetags import tramite_tags, tramite_literal

class TableAsJSON(JSONResponseMixin, View):
  model = Tramite

  def get(self, request, *args, **kwargs):
    col_name_map = {
      '0': 'numero',
      '1': 'tipo_tramite',
      '2': 'estado',
      '3': 'titulo',
      '4': 'parte',
      '5': 'contra_parte',
      '6': 'acciones',
    }
    object_list = self.model.objects.all()
    search_text = request.GET.get('sSearch', '').lower()
    start = int(request.GET.get('iDisplayStart', 0))
    delta = int(request.GET.get('iDisplayLength', 50))
    sort_dir = request.GET.get('sSortDir_0', 'asc')
    sort_col = int(request.GET.get('iSortCol_0', 0))
    sort_col_name = request.GET.get('mDataProp_%s' % sort_col, '1')
    sort_dir_prefix = (sort_dir == 'desc' and '-' or '')

    if sort_col_name in col_name_map:
      sort_col = col_name_map[sort_col_name]
      object_list = object_list.order_by('%s%s' % (sort_dir_prefix, sort_col))

    filtered_object_list = object_list
    if len(search_text) > 0:
      filtered_object_list = object_list.filter_on_search(search_text)

    json = {
      "iTotalRecords": object_list.count(),
      "iTotalDisplayRecords": filtered_object_list.count(),
      "sEcho": request.GET.get('sEcho', 1),
      "aaData": [obj.as_list() for obj in filtered_object_list[start:(start+delta)]]
    }
    return self.render_json_response(json)

# Create your views here.
class IndexView(ListView):
  template_name = 'tramite/index.html'
  model = Tramite
  context_object_name = 'tramites'

class TramiteRegistrar(CreateView):
  model = Tramite
  form_class = TramiteForm
  template_name = 'tramite/ajax/registrar.html'
  
  def form_valid(self, form):
    instancia = form.save(commit=False)
    instancia.usuario = self.request.user
    instancia.save()
    context = {'tramite_id': instancia.id,}
    return render(self.request, 'tramite/ajax/notificacion.html', context)

class TramiteAjax(View):
  def get(self, *args, **kwargs):
    tramite = Tramite.objects.get(pk=kwargs.get('id', "any_default"))
    firma = tramite.tramitepersona_set.filter(firma=True, testigo=False)
    nofirma = tramite.tramitepersona_set.filter(firma=False, testigo=False)
    testigo = tramite.tramitepersona_set.filter(firma=True, testigo=True)
    resultado = tramite_tags.tramitantes(firma, nofirma, testigo)
    return JsonResponse({
      'paginas': len(resultado)
    }, content_type='application/json')


class TramiteEditar(UpdateView):
  model = Tramite
  form_class = TramiteForm
  template_name = 'tramite/editar.html'
  context_object_name = 'tramite'


  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    formFirmante = TramitePersonaForm(initial={'tramite':self.object.pk})
    formViaje = TramiteViajeForm(initial={'tramite':self.object.pk})
    tramite = Tramite.objects.get(pk=self.object.pk)
    context['formfirmante'] = formFirmante
    context['formviaje'] = formViaje
    return context

  def form_valid(self, form):
    model = self.model
    model = form.save(commit=False)
    model.usuario = self.request.user
    hoy = datetime.now()
    if model.numero == 0:
      print("llego aca")
      try:
        numero = Numerotramite.objects.get(tipo=model.tipo_tramite,gestion=hoy.year)
        numero.numero = numero.numero + 1
      except Numerotramite.DoesNotExist:
        numero = Numerotramite(numero=1, gestion=hoy.year, tipo=model.tipo_tramite)
      model.numero = numero.numero
      model.gestion = numero.gestion
      model.fecha_registro = date(hoy.year,hoy.month,hoy.day)
      model.hora_registro = time(hoy.hour, hoy.minute, hoy.second)
      model.estado = True
      numero.save()
    model.save()
    self.partes(model)
    return JsonResponse({'status': 200, 'mensaje': 'Se ha Guardado con Exito la Informacion'}, content_type='application/json')


  def partes(self, tramite):
    tramitepersonas = Tramitepersona.objects.filter(tramite=tramite.id)
    auxp = tramite.parte_aux
    auxcp = ''
    for item in tramitepersonas:
      if item.contra_parte:
        if auxcp:
          auxcp = auxcp+',%s %s %s' % (item.persona.nombres, item.persona.apellido_pat, item.persona.apellido_mat)
        else:
          auxcp = '%s %s %s' % (item.persona.nombres, item.persona.apellido_pat, item.persona.apellido_mat)
      else:
        if auxp:
          auxp = auxp+',%s %s %s' % (item.persona.nombres, item.persona.apellido_pat, item.persona.apellido_mat)
        else:
          auxp = '%s %s %s' % (item.persona.nombres, item.persona.apellido_pat, item.persona.apellido_mat)
      print(auxcp)
      print(auxp)
    tramite.parte = auxp
    tramite.contra_parte = auxcp
    tramite.save()

class TramiteEliminar(DeleteView):
  model = Tramite
  context_object_name = 'tramite'
  template_name = 'tramite/eliminar.html'
  def delete(self, request, *args, **kwargs):
    model = self.get_object()
    model.delete()
    return JsonResponse({'status': 200, 'mensaje': 'Se ha Eliminado con Exito la Informacion'}, content_type='application/json')

class PersonaAutocomplete(View):
  def get(self, *args, **kwargs):
    q = self.request.GET['q']
    qs = Persona.objects.filter(Q(nombres__icontains=q) | Q(apellido_pat__icontains=q) | Q(apellido_mat__icontains=q) | Q(nro_documento__istartswith=q))
    qs = self.get_results(qs)        
    return JsonResponse({
      'results': qs
    }, content_type='application/json')

  def get_results(self, results):
    return [dict(id=x.id, text=x.nombres+' '+x.apellido_pat+' '+x.apellido_mat+' - '+x.nro_documento) for x in results]

class CreateTramitePersona(CreateView):
  model = Tramitepersona
  form_class = TramitePersonaForm

  def form_valid(self, form):
    model = form.save(commit=False)
    tramite = Tramite.objects.get(pk=model.tramite.id)
    if not Tramitepersona.objects.filter(tramite=model.tramite.id, persona=model.persona.id).exists():
      model.save()
      self.partes(tramite)
    return render(self.request, 'tramite/ajax/firmantes.html', context={'tramite': tramite })

  def partes(self, tramite):
    tramitepersonas = Tramitepersona.objects.filter(tramite=tramite.id)
    auxp = tramite.parte_aux
    auxcp = ''
    for item in tramitepersonas:
      if item.contra_parte:
        if auxcp:
          auxcp = auxcp+',%s %s %s' % (item.persona.nombres, item.persona.apellido_pat, item.persona.apellido_mat)
        else:
          auxcp = '%s %s %s' % (item.persona.nombres, item.persona.apellido_pat, item.persona.apellido_mat)
      else:
        if auxp:
          auxp = auxp+',%s %s %s' % (item.persona.nombres, item.persona.apellido_pat, item.persona.apellido_mat)
        else:
          auxp = '%s %s %s' % (item.persona.nombres, item.persona.apellido_pat, item.persona.apellido_mat)
    tramite.parte = auxp
    tramite.contra_parte = auxcp
    tramite.save()

class CreateTramiteViaje(CreateView):
  model = Tramiteviaje
  form_class = TramiteViajeForm

  def form_valid(self, form):
    model = form.save(commit=False)
    tramite = Tramite.objects.get(pk=model.tramite.id)
    if not Tramiteviaje.objects.filter(tramite=model.tramite.id, persona=model.persona.id).exists():
      model.save()
      self.partes(tramite)
    return render(self.request, 'tramite/ajax/menorviaje.html', context={'tramite': tramite })
    
  def partes(self, tramite):
    tramitepersonas = Tramiteviaje.objects.filter(tramite=tramite.id)
    auxp = tramite.parte_aux
    auxcp = ''
    for item in tramitepersonas:
      if not item.tipo:
        if auxcp:
          auxcp = auxcp+',%s %s %s' % (item.persona.nombres, item.persona.apellido_pat, item.persona.apellido_mat)
        else:
          auxcp = '%s %s %s' % (item.persona.nombres, item.persona.apellido_pat, item.persona.apellido_mat)
      else:
        if auxp:
          auxp = auxp+',%s %s %s' % (item.persona.nombres, item.persona.apellido_pat, item.persona.apellido_mat)
        else:
          auxp = '%s %s %s' % (item.persona.nombres, item.persona.apellido_pat, item.persona.apellido_mat)
    tramite.parte = auxp
    tramite.contra_parte = auxcp
    tramite.save()

class DeleteTramitePersona(DeleteView):
  model = Tramitepersona
  context_object_name = 'tramitepersona'

  def delete(self, request, *args, **kwargs):
    model = self.get_object()
    tramite = Tramite.objects.get(pk=model.tramite.id)
    model.delete()
    self.partes(tramite)
    return render(self.request, 'tramite/ajax/firmantes.html', context={'tramite': tramite })

  def partes(self, tramite):
    tramitepersonas = Tramitepersona.objects.filter(tramite=tramite.id)
    auxp = tramite.parte_aux
    auxcp = ''
    for item in tramitepersonas:
      if item.contra_parte:
        if auxcp:
          auxcp = auxcp+',%s %s %s' % (item.persona.nombres, item.persona.apellido_pat, item.persona.apellido_mat)
        else:
          auxcp = '%s %s %s' % (item.persona.nombres, item.persona.apellido_pat, item.persona.apellido_mat)
      else:
        if auxp:
          auxp = auxp+',%s %s %s' % (item.persona.nombres, item.persona.apellido_pat, item.persona.apellido_mat)
        else:
          auxp = '%s %s %s' % (item.persona.nombres, item.persona.apellido_pat, item.persona.apellido_mat)
    tramite.parte = auxp
    tramite.contra_parte = auxcp
    tramite.save()

class DeleteTramiteViaje(DeleteView):
  model = Tramiteviaje
  context_object_name = 'tramitepersona'

  def delete(self, request, *args, **kwargs):
    model = self.get_object()
    tramite = Tramite.objects.get(pk=model.tramite.id)
    model.delete()
    self.partes(tramite)
    return render(self.request, 'tramite/ajax/menorviaje.html', context={'tramite': tramite })

  def partes(self, tramite):
    tramitepersonas = Tramiteviaje.objects.filter(tramite=tramite.id)
    auxp = tramite.parte_aux
    auxcp = ''
    for item in tramitepersonas:
      if not item.tipo:
        if auxcp:
          auxcp = auxcp+',%s %s %s' % (item.persona.nombres, item.persona.apellido_pat, item.persona.apellido_mat)
        else:
          auxcp = '%s %s %s' % (item.persona.nombres, item.persona.apellido_pat, item.persona.apellido_mat)
      else:
        if auxp:
          auxp = auxp+',%s %s %s' % (item.persona.nombres, item.persona.apellido_pat, item.persona.apellido_mat)
        else:
          auxp = '%s %s %s' % (item.persona.nombres, item.persona.apellido_pat, item.persona.apellido_mat)
    tramite.parte = auxp
    tramite.contra_parte = auxcp
    tramite.save()

class ReportTramitePdf(View):

  def cabecera(self,pdf):
    #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
    pdf.setFont("Times-Bold", 16)
    #Dibujamos una cadena en la ubicación X,Y especificada
    pdf.drawString(260, 860, str(self.tramite.numero)+'/'+str(self.tramite.gestion))
    pdf.setFont("Times-Roman", 10)
    pdf.drawString(325, 860, '('+tramite_literal.main(self.tramite.numero)+')')
    pdf.drawString(205, 845, tramite_tags.titulouno(self.tramite.titulo))
    pdf.drawString(100, 830, tramite_tags.titulodos(self.tramite.titulo))
    pdf.drawString(425, 830, tramite_tags.fechaupper(self.tramite.fecha_documento))
    pdf.drawString(200, 800, u"ORURO")
    pdf.drawString(480, 800, tramite_tags.horareg(self.tramite.hora_registro))
    pdf.drawString(115, 785, tramite_tags.diaupper(self.tramite.fecha_registro.strftime("%A"))+' '+tramite_literal.main(self.tramite.fecha_registro.day))
    pdf.drawString(270, 785, tramite_tags.mesupper(self.tramite.fecha_registro.month))
    pdf.drawString(380, 785, tramite_literal.main(self.tramite.fecha_registro.year))
    pdf.drawString(280, 765, "(4) CUATRO")
    pdf.drawString(460, 765, "ORURO")
    pdf.drawString(240, 745, "WILLIAM DELGADO TOLEDO.-")

  def firmantes(self, pdf):
    pdf.setFont("Times-Roman", 10)
    fir = self.resaux[0]
    nfr = self.resaux[1]
    tes = self.resaux[2]
    i = 0
    while i < 4: 
      if fir[i] == None:
        pdf.drawCentredString(165,725-i*32, "&&&&&&&&&&&&&&&&&")
        pdf.drawCentredString(289,725-i*32, "&&&&&&&&&&&&")
        pdf.drawCentredString(400,725-i*32, "&&&&&&&&&&&&")
        pdf.drawCentredString(517,725-i*32, "&&&&&&&&&")   
      else:
        pdf.drawCentredString(165,725-i*32, fir[i].persona.nombres)  
        pdf.drawCentredString(290,725-i*32, fir[i].persona.apellido_pat)
        pdf.drawCentredString(400,725-i*32, fir[i].persona.apellido_mat)
        pdf.drawCentredString(517,725-i*32, fir[i].persona.nro_documento + ' '+ tramite_tags.expedido(fir[i].persona.expedido))
      i = i + 1
    
    if fir[0] == None:
      pdf.setFont("Times-Roman", 50)
      pdf.drawCentredString(278,532, "X")
      pdf.setFont("Times-Roman", 10)
      pdf.drawCentredString(177,520, "&&&&&&&&&&&&&&&&&")  
    if fir[1] == None:
      pdf.setFont("Times-Roman", 50)
      pdf.drawCentredString(502,532, "X")
      pdf.setFont("Times-Roman", 10)
      pdf.drawCentredString(402,550, "&&&&&&&&&&&&&&&&&")  
    if fir[2] == None:
      pdf.setFont("Times-Roman", 50)
      pdf.drawCentredString(278,478, "X")
      pdf.setFont("Times-Roman", 10)
      pdf.drawCentredString(177,500, "&&&&&&&&&&&&&&&&&")  
    if fir[3] == None:
      pdf.setFont("Times-Roman", 50)
      pdf.drawCentredString(502,478, "X")
      pdf.setFont("Times-Roman", 10)
      pdf.drawCentredString(402,500, "&&&&&&&&&&&&&&&&&")  
    i = 0
    while i < 2: 
      if nfr[i] == None:
        pdf.drawCentredString(162,410-i*32, "&&&&&&&&&&&&&&&")  
        pdf.drawCentredString(275,410-i*32, "&&&&&&&&&&&&")
        pdf.drawCentredString(377,410-i*32, "&&&&&&&&&&&&")
        pdf.drawCentredString(507,410-i*32, "&&&&&&&&&&&&")
      else:
        pdf.drawCentredString(162,410-i*32, nfr[i].persona.nombres)  
        pdf.drawCentredString(275,410-i*32, nfr[i].persona.apellido_pat)
        pdf.drawCentredString(377,410-i*32, nfr[i].persona.apellido_mat)
        pdf.drawCentredString(507,410-i*32, nfr[i].persona.nro_documento + ' '+ tramite_tags.expedido(nfr[i].persona.expedido))
      i = i + 1
    if nfr[0] == None:
      pdf.setFont("Times-Roman", 50)
      pdf.drawCentredString(195,297, "X")
      pdf.drawCentredString(258,297, "X")
      pdf.setFont("Times-Roman", 10)
    if nfr[1] == None:
      pdf.setFont("Times-Roman", 50)
      pdf.drawCentredString(375,297, "X")
      pdf.drawCentredString(440,297, "X")
      pdf.setFont("Times-Roman", 10)
    
    i = 0
    while i < 2:
      if tes[i] == None:
        pdf.drawCentredString(208,260-i*32, "&&&&&&&&&&&&&&&&&&&&")
        pdf.drawCentredString(345,260-i*32, "&&&&&&&&&&&")
        pdf.drawCentredString(435,260-i*32, "&&&&&&&&&&&")
        pdf.setFont("Times-Roman", 50)
        pdf.drawCentredString(520,250-i*55, "X")
        pdf.setFont("Times-Roman", 10)
      else:
        pdf.setFont("Times-Roman", 8)
        pdf.drawCentredString(208,260-i*32, tes[i].persona.nombres+' '+tes[i].persona.apellido_pat+' '+tes[i].persona.apellido_mat)
        pdf.drawCentredString(345,260-i*32, tes[i].persona.nro_documento+ ' '+tramite_tags.expedido(tes[i].persona.expedido))
        pdf.setFont("Times-Roman", 10)
      i = i + 1

    qrw = QrCodeWidget('NOTARIA DE FE PUBLICA N4|'+(str(self.tramite.numero) + '|' + str(self.tramite.gestion)).upper()+'|CFYR'+'|ORURO|BOLIVIA')
    b = qrw.getBounds()
    w=b[2]-b[0] 
    h=b[3]-b[1] 
    d = Drawing(50,50,transform=[50./w,0,0,50./h,0,0]) 
    d.add(qrw)
    renderPDF.draw(d, pdf, 100, 140)

  def get(self, request, *args, **kwargs):
    self.tramite = Tramite.objects.get(pk=kwargs.get('id', "any_default"))
    #Indicamos el tipo de contenido a devolver, en este caso un pdf
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "tramite.pdf"  # llamado clientes
    response['Content-Disposition'] = 'inline; filename=%s' % pdf_name
    #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
    buffer = BytesIO()
    #Canvas nos permite hacer el reporte con coordenadas X y Y
    pdf = canvas.Canvas(buffer, pagesize=legal)
    self.firma = self.tramite.tramitepersona_set.filter(firma=True, testigo=False)
    self.nofirma = self.tramite.tramitepersona_set.filter(firma=False, testigo=False)
    self.testigo = self.tramite.tramitepersona_set.filter(firma=True, testigo=True)
    self.resultado = tramite_tags.tramitantes(self.firma, self.nofirma, self.testigo)
    #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
    self.resaux = []
    i = 0
    while i < len(self.resultado):
      self.resaux = self.resultado[i]
      self.cabecera(pdf)
      self.firmantes(pdf)
      pdf.showPage()
      self.cabecera(pdf)
      self.firmantes(pdf)
      pdf.showPage()
      i = i + 1
    #y = 600
    #self.tabla(pdf, y)
    #Con show page hacemos un corte de página para pasar a la siguiente
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


class ReporteViajePdf(View):
  y = 950
  def cabecera(self,pdf):
    #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
    pdf.setFont("Times-Bold", 12)
    pdf.drawString(50, self.y, "ESTADO PLURINACIONAL DE BOLIVIA")
    self.y = self.y-50
    pdf.drawString(50, self.y, "AUTORIZACION DE ViAJE DE MENOR")
    self.y = self.y-15
    pdf.drawString(55, self.y, "NUMERO DE AUTORIZACION:")
    pdf.setFont("Times-Roman", 12)
    pdf.drawString(235, self.y, str(self.tramite.numero)+'/'+str(self.tramite.gestion))
    pdf.setFont("Times-Roman", 10)
    self.y = self.y-15
    pdf.drawCentredString(165, self.y, "Fecha: "+tramite_tags.fechaupper(self.tramite.fecha_documento))

  def menor(self, pdf):
    menor = self.tramite.tramiteviaje_set.filter(tipo=True)
    pdf.setFont("Times-Bold", 12)
    self.y = self.y-60
    pdf.drawString(50, self.y, "I. DATOS DEL NIÑO NIÑA ADOLESCENTE")
    pdf.setFont("Times-Roman", 10)
    self.y = self.y-40
    pdf.drawString(50, self.y, "Nombre: "+menor[0].persona.nombres+" "+menor[0].persona.apellido_pat+" "+menor[0].persona.apellido_mat)
    pdf.drawString(350, self.y, "Edad: "+tramite_tags.edad(menor[0].persona.fecha_nacimiento))
    self.y = self.y-12
    pdf.drawString(50, self.y, "Documento: "+menor[0].persona.nro_documento+" "+tramite_tags.expedido(menor[0].persona.expedido))
    pdf.drawString(350, self.y, "Telefono: "+menor[0].persona.telefono)
    self.y = self.y-12
    pdf.drawString(50, self.y, "Certificado de Nacimiento: "+menor[0].certificado_nacimiento)
    pdf.drawString(350, self.y, "Residencia de Viaje: "+menor[0].residencia_viaje)
    self.y = self.y-12
    pdf.drawString(50, self.y, "Domicilio: "+menor[0].persona.direccion)
    pdf.drawString(350, self.y, "Tiempo de Ausencia: "+str(menor[0].tiempo_ausencia))
    self.y = self.y-12
    pdf.drawString(50, self.y, "Destino: "+menor[0].destino)
    pdf.drawString(350, self.y, "Fecha de Retorno: "+tramite_tags.fechaupper(menor[0].fecha_retorno))
    self.y = self.y-12
    pdf.drawString(50, self.y, "Motivo de viaje: "+menor[0].motivo_viaje)
    pdf.drawString(350, self.y, "Objeto de viaje: "+menor[0].objeto_viaje)

  def padres(self, pdf):
    padres = self.tramite.tramiteviaje_set.filter(tipo=False)
    menor = self.tramite.tramiteviaje_set.filter(tipo=True)
    padre_trab = ''
    madre_trab = ''
    if padres[0].persona.genero:
      padre = padres[0].persona
      padre_trab = padres[0].lugar_trabajo
      madre = padres[1].persona
      madre_trab = padres[1].lugar_trabajo
    else:
      padre = padres[1].persona
      padre_trab = padres[1].lugar_trabajo
      madre = padres[0].persona
      madre_trab = padres[0].lugar_trabajo

    if padres[0].acompanante:
      acompanante = padres[0].persona
    else:
      acompanante = padres[1].persona

    pdf.setFont("Times-Bold", 12)
    self.y = self.y-60
    pdf.drawString(50, self.y, "II. AUTORIZACION DE LOS PADRES")
    pdf.setFont("Times-Roman", 10)
    self.y = self.y-40
    pdf.drawString(50, self.y, "Yo: "+padre.nombres+" "+padre.apellido_pat+" "+padre.apellido_mat)
    pdf.drawString(350, self.y, "Yo: "+madre.nombres+" "+madre.apellido_pat+" "+madre.apellido_mat)
    self.y = self.y-12
    pdf.drawString(50, self.y, "Documento: "+padre.nro_documento+" "+tramite_tags.expedido(padre.expedido))
    pdf.drawString(350, self.y, "Documento: "+madre.nro_documento+" "+tramite_tags.expedido(padre.expedido))
    self.y = self.y-12
    pdf.drawString(50, self.y, "Estado Civil: "+tramite_tags.estadocivil(padre.estado_civil))
    pdf.drawString(350, self.y, "Estado Civil: "+tramite_tags.estadocivil(madre.estado_civil))
    self.y = self.y-12
    pdf.drawString(50, self.y, "Lugar de Trabajo: "+padre_trab)
    pdf.drawString(350, self.y, "Lugar de Trabajo: "+madre_trab)
    self.y = self.y-40
    pdf.drawString(50, self.y, "Autorizamos el viaje del menor:")
    pdf.drawCentredString(350, self.y, menor[0].persona.nombres+" "+menor[0].persona.apellido_pat+" "+menor[0].persona.apellido_mat)
    self.y = self.y-15
    pdf.drawString(50, self.y, "Siendo el progenitor acompañante:")
    pdf.drawCentredString(350, self.y, acompanante.nombres+" "+acompanante.apellido_pat+" "+acompanante.apellido_mat)
    self.y = self.y-15
    pdf.drawString(250, self.y, "Con No. de C.I.: "+acompanante.nro_documento+" "+tramite_tags.expedido(acompanante.expedido))
    pdf.drawString(400, self.y, tramite_tags.progenitor(acompanante.genero))
    self.y = self.y-80
    pdf.drawCentredString(180, self.y, "Firma: ............................. Huella pulgar: ......................")
    pdf.drawCentredString(420, self.y, "Firma: ............................. Huella pulgar: ......................")
    self.y = self.y-20
    pdf.drawCentredString(180, self.y, padre.nombres+" "+padre.apellido_pat+" "+padre.apellido_mat)
    pdf.drawCentredString(420, self.y, madre.nombres+" "+madre.apellido_pat+" "+madre.apellido_mat)
    self.y = self.y-15
    pdf.drawCentredString(180, self.y, "Aclaracion de firma")
    pdf.drawCentredString(420, self.y, "Aclaracion de firma")

    pdf.setFont("Times-Bold", 12)
    self.y = self.y-50
    pdf.drawString(50, self.y, "III. AUTORIZACION DEL NOTARIO EN LA VIA VOLUNTARIA NOTARIAL")
    pdf.setFont("Times-Roman", 10)
    self.y = self.y-30
    pdf.drawString(50, self.y, "Cumplidos los requisitos señalados por Ley 483 inc. B) y Decreto Reglamentario 2189 Art. 102 y 103; Yo: Abg. William Delgado")
    self.y = self.y-12
    pdf.drawString(50, self.y, "Toledo, Notario de Fe Publica No. 04 del Municipio de Oruro, Departamento de Oruro, del Estado Plurinacional de Bolivia, Autorizo")
    self.y = self.y-12
    pdf.drawString(50, self.y, "el viaje del menor, por el tiempo señalado en el presente documento, es todo lo que doy Fe y Certifico, Firma y Signo.")
    self.y = self.y-40
    pdf.drawString(50, self.y, "Lugar y Fecha: ORURO "+tramite_tags.fechaupper(self.tramite.fecha_documento))
    self.y = self.y-80
    pdf.setFont("Times-Roman", 12)
    pdf.drawCentredString(450, self.y, "Firma y Sello")
    self.y = self.y-15
    pdf.setFont("Times-Bold", 12)
    pdf.drawCentredString(450, self.y, "NOTARIO DE FE PUBLICA")
    self.y = self.y-40
    pdf.setFont("Times-Roman", 10)
    pdf.drawString(50, self.y, "Este Formulario tiene validez de 90 dias a partir de la fecha de autorizacion del Notario.")
    self.y = self.y-20
    pdf.setFont("Times-Bold", 10)
    pdf.drawString(50, self.y, "Nota: LAS AUTORIZACIONES DEL VIAJE SON EXCLUSIVAS PARA EL LUGAR DE DESTINO Y POR EL TIEMPO")
    self.y = self.y-12
    pdf.drawString(50, self.y, "SEÑALADO")
    pdf.setFont("Times-Roman", 10)
    pdf.drawString(110, self.y, "por el cual no pueden ser utilizadas para quedarse en lugares intermedios, siendo el presente formulario utilizado en")
    self.y = self.y-12
    pdf.drawString(50, self.y, "cumplimiento al instructivo")
    pdf.setFont("Times-Bold", 10)
    pdf.drawString(165, self.y, "002/2015")
    pdf.setFont("Times-Roman", 10)
    pdf.drawString(205, self.y, "de la")
    pdf.setFont("Times-Bold", 10)
    pdf.drawString(225, self.y, "DIRECCION DEL NOTARIADO PLURINACIONAL.")
    qrw = QrCodeWidget('NOTARIA DE FE PUBLICA N4|'+(str(self.tramite.numero) + '|' + str(self.tramite.gestion)).upper()+'|AUTORIZACION VIAJE MENOR'+'|ORURO|BOLIVIA')
    b = qrw.getBounds()
    w=b[2]-b[0] 
    h=b[3]-b[1] 
    d = Drawing(60,60,transform=[50./w,0,0,50./h,0,0]) 
    d.add(qrw)
    renderPDF.draw(d, pdf, 100, 150)

  def get(self, request, *args, **kwargs):
    self.tramite = Tramite.objects.get(pk=kwargs.get('id', "any_default"))
    #Indicamos el tipo de contenido a devolver, en este caso un pdf
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "tramite.pdf"  # llamado clientes
    response['Content-Disposition'] = 'inline; filename=%s' % pdf_name
    #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
    buffer = BytesIO()
    #Canvas nos permite hacer el reporte con coordenadas X y Y
    pdf = canvas.Canvas(buffer, pagesize=legal)
    self.cabecera(pdf)
    self.menor(pdf)
    self.padres(pdf)
    #y = 600
    #self.tabla(pdf, y)
    #Con show page hacemos un corte de página para pasar a la siguiente
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response