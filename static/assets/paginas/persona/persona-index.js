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
    },
    "bServerSide": true,
    "sAjaxSource": "/persona/as_json"
  });

  $("#registro-paciente").click(function(){
    $.ajax({
      url: 'registrar',
      type: 'get',  
      success: function(data){
          $('#contenido-modal').html(data);
      }
    })
  });
  
  $("#myTable").on('click', '.editar-persona', function(){
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
});