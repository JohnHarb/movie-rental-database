function printMovies(x)
{
  $("#mes").html(" ");
  $("#mov1").html(" ");
  x = JSON.parse(x);
  for (i of x)
  {
    row = '<tr><td>'+i.mname+'</td><td>'+i.copies+'</td><td><button class="plus" id="'+i.mname+'">+</button><button class="sub" id="'+i.mname+'">-</button></td></tr>'
    $("#mov1").html($("#mov1").html()+row);
  }
  $(".plus").on("click", plusHandle);
  $(".sub").on("click", subHandle);
}

function callback(x) {
  if (x["message"] == "0")
  {
    $("#mes").html("enter a valid movie");
  }
  else
  {
    printMovies(x);
  }
}

function plusHandle(e) {
  var movie = e.target.id;
  out = {movie:movie,action:"add"};
  $.post("/dbMovie/", out, callback);
}

function addHandle() 
{
  var movie = $("#movie").val();
  out = {movie:movie,action:"new"};
  $.post("/dbMovie/", out, callback);
}

function subHandle(e) {
  var movie = e.target.id;
  out = {movie:movie,action:"remove"};
  $.post("/dbMovie/", out, callback);
}

$(document).ready(function(){$.get("/dbMovie/", {}, callback);});
$("#add").on("click", addHandle);