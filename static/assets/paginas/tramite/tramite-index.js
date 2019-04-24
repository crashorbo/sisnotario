$(document).ready(function(){
  $('#myTable').DataTable({
    "language": {
      "sProcessing":     "Procesando...",
      "sLengthMenu":     "Mostrar _MENU_ registros",
      "sZeroRecords":    "No se encontraron resultados",
      "sEmptyTable":     "Ningún dato disponible en esta tabla",
      "sInfo":           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
      "sInfoEmpty":      "Mostrando registros del 0 al 0 de un total de 0 registros",
      "sInfoFiltered":   "(filtrado de un total de _MAX_ registros)",
      "sInfoPostFix":    "",
      "sSearch":         "Buscar:",
      "sUrl":            "",
      "sInfoThousands":  ",",
      "sLoadingRecords": "Cargando...",
      "oPaginate": {
        "sFirst":    "Primero",
        "sLast":     "Último",
        "sNext":     "Siguiente",
        "sPrevious": "Anterior"
      },
      "oAria": {
        "sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
        "sSortDescending": ": Activar para ordenar la columna de manera descendente"
      }
    }
  });

  $("#registro-tramite").click(function(){
    $.ajax({
      url: 'registrar',
      type: 'get',  
      success: function(data){
          $('#contenido-modal').html(data);
      }
    })
  });
  
  $(".editar-persona").click(function(){
    var thisurl = $(this).attr('data-url');
    $.ajax({
      url: thisurl,
      type: 'get',  
      success: function(data){
          $('#contenido-modal').html(data);
          $('#responsive-modal').modal('show');
      }
    })
  });

  $('#responsive-modal').on('hidden.bs.modal', function (e) {
    location.reload();
  })

  $('.tramite-eliminar').on('submit', function (e) {
    e.preventDefault();
    var $formData = $(this).serialize();
    var $formArray = $(this).serializeArray();
    var $formArray = {};
    $.each($(this).serializeArray(), function (i, field) {
      $formArray[field.name] = field.value; 
    });
    var $thisUrl = $(this).attr('action');
    var $thisMethod = $(this).attr('method');
    $.ajax({
        method: $thisMethod,
        url: $thisUrl,
        data: $formData,
        success: function(data){
          location.reload();
        },
        error: function(xhr,errmsg,err) {
          // Show an error
          $('#results').html("<div class='alert-box alert radius' data-alert>"+
          "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    })
  });
});

$('#responsive-modal').on('change', '#id_tipo_tramite', function(e){
  if ($(this).val() == 1)
  {
    $('#tipouno').show();
  }
  if ($(this).val() == 2)
  {
    $('#tipouno').hide();
  }
});

$("#form-persona").on('submit', function(e) {
  e.preventDefault();
  $('#guardarcfyr').attr('disabled', true);
  this.submit(); 
});