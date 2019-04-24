$(document).ready(function(){

  $('.fecha').datepicker({
    autoclose: true,
    todayHighlight: true,
    format: "dd/mm/yyyy",
    language: "es",
  });

  $('.select2').select2({
    language: 'es',
    placeholder: "Seleccionar Persona",
    ajax: {
      url: Urls.persona_autocomplete(),
      dataType: 'json',
      delay: 250,
      data: function(params) {
        return {
          q: params.term, // search term
          page: params.page
        };
      },
      processResults: function(data, params) {
          // parse the results into the format expected by Select2
          // since we are using custom formatting functions we do not need to
          // alter the remote JSON data, except to indicate that infinite
          // scrolling can be used
          params.page = params.page || 1;
          return {
              results: data.results,
              pagination: {
                  more: (params.page * 30) < data.total_count
              }
          };
      },
    cache: true
    },
    escapeMarkup: function(markup) {
        return markup;
    }, // let our custom formatter work
    minimumInputLength: 2,
    
  });
  
  document.addEventListener('keypress', function(evt) {

    // Si el evento NO es una tecla Enter
    if (evt.key !== 'Enter') {
      return;
    }
    
    let element = evt.target;
  
    // Si el evento NO fue lanzado por un elemento con class "focusNext"
    if (!element.classList.contains('focusNext')) {
      return;
    }
  
    // AQUI logica para encontrar el siguiente
    let tabIndex = element.tabIndex + 1;
    var next = document.querySelector('[tabindex="'+tabIndex+'"]');
  
    // Si encontramos un elemento
    if (next) {
      next.focus();
      event.preventDefault();
    }
  });

  $('#form-tramitante').on('submit', function (e) {
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
          $("#tramitantes").html(data);
          $(".select2").val("").trigger("change");
        },
        error: function(xhr,errmsg,err) {
          // Show an error
          $('#results').html("<div class='alert-box alert radius' data-alert>"+
          "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    })
  });
  $('#form-editar').on('submit', function(e){
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

  $("#registro-persona").click(function(e){
    e.preventDefault();
    $.ajax({
      url: Urls.persona_registrar(),
      type: 'get',  
      success: function(data){
          $('#contenido-modal').html(data);
          $('#responsive-modal').modal('show');
      }
    })
  });
  $("#tramitantes").on('click', '.editar-persona',function(){
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

  $('#tramitantes').on('submit', '.form-eliminar', function (e) {
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
          $('#tramitantes').html(data);
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

function imprimirlista(e, obj)
{
  e.preventDefault();
  this_url = $(obj).attr('href');
  window.open(this_url,"reporte","height=500,width=700,status=no, toolbar=no,menubar=no,location=no,scrollbars=yes");
}

$("#form-editar").on('submit', function(e) {
  e.preventDefault();
  $('#guardarcfyr').attr('disabled', true);
  this.submit(); 
});