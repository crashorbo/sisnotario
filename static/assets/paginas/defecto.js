'use strict';

$("input").keyup(function(){
  this.value = this.value.toUpperCase();
});

$("textarea").keyup(function(){
  this.value = this.value.toUpperCase();
});