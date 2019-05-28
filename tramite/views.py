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

from django.contrib.auth.models import User
from .models import Tramite, Tramitepersona, Numerotramite
from persona.models import Persona
from .forms import TramiteForm, TramitePersonaForm, TramiteViajeForm
from .templatetags import tramite_tags, tramite_literal

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
    firma = tramite.tramitepersona_set.filter(firma=True, testigo=False)
    nofirma = tramite.tramitepersona_set.filter(firma=False, testigo=False)
    testigo = tramite.tramitepersona_set.filter(firma=True, testigo=True)
    resultado = tramite_tags.tramitantes(firma, nofirma, testigo)
    context['paginas'] = len(resultado)
    context['formfirmante'] = formFirmante
    context['formviaje'] = formViaje
    return context

  def form_valid(self, form):
    model = self.model
    model = form.save(commit=False)
    model.usuario = self.request.user
    hoy = datetime.now()
    if not model.estado:
      try:
        numero = Numerotramite.objects.get(tipo=model.tipo_tramite,gestion=hoy.year)
        numero.numero = numero.numero + 1
        numero.save()
        model.numero = numero.numero
        model.gestion = numero.gestion
        model.fecha_registro = date(hoy.year,hoy.month,hoy.day)
        model.hora_registro = time(hoy.hour, hoy.minute, hoy.second)
        model.estado = True
      except Numerotramite.DoesNotExist:
        numero = Numerotramite(numero=1, gestion=hoy.year, tipo=model.tipo_tramite)
        model.numero = numero.numero
        model.gestion = numero.gestion
        model.fecha_registro = date(hoy.year,hoy.month,hoy.day)
        model.hora_registro = time(hoy.hour, hoy.minute, hoy.second)
        model.estado = True
        numero.save()
    model.save()
    return JsonResponse({'status': 200, 'mensaje': 'Se ha Guardado con Exito la Informacion'}, content_type='application/json')

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
    return render(self.request, 'tramite/ajax/firmantes.html', context={'tramite': tramite })

class DeleteTramitePersona(DeleteView):
  model = Tramitepersona
  context_object_name = 'tramitepersona'

  def delete(self, request, *args, **kwargs):
    model = self.get_object()
    tramite = Tramite.objects.get(pk=model.tramite.id)
    model.delete()
    return render(self.request, 'tramite/ajax/firmantes.html', context={'tramite': tramite })

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
        pdf.drawCentredString(165,725-i*32, "=======================")
        pdf.drawCentredString(289,725-i*32, "===================")
        pdf.drawCentredString(400,725-i*32, "==================")
        pdf.drawCentredString(517,725-i*32, "============")   
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
      pdf.drawCentredString(177,520, "=======================")  
    if fir[1] == None:
      pdf.setFont("Times-Roman", 50)
      pdf.drawCentredString(502,532, "X")
      pdf.setFont("Times-Roman", 10)
      pdf.drawCentredString(402,550, "=======================")  
    if fir[2] == None:
      pdf.setFont("Times-Roman", 50)
      pdf.drawCentredString(278,478, "X")
      pdf.setFont("Times-Roman", 10)
      pdf.drawCentredString(177,500, "=======================")  
    if fir[3] == None:
      pdf.setFont("Times-Roman", 50)
      pdf.drawCentredString(502,478, "X")
      pdf.setFont("Times-Roman", 10)
      pdf.drawCentredString(402,500, "=======================")  
    i = 0
    while i < 2: 
      if nfr[i] == None:
        pdf.drawCentredString(162,410-i*32, "====================")  
        pdf.drawCentredString(275,410-i*32, "==================")
        pdf.drawCentredString(377,410-i*32, "=================")
        pdf.drawCentredString(507,410-i*32, "=================")
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
        pdf.drawCentredString(208,260-i*32, "==========================")
        pdf.drawCentredString(345,260-i*32, "===========")
        pdf.drawCentredString(435,260-i*32, "===========")
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
