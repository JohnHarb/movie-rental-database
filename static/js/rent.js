function printMovies(x)
{
  $("#mes").html("");
  $("#mov2").html("");
  x = JSON.parse(x);
  
  for (i of x)
  {
    row = '<tr><td><button class="umovie" id="'+i.movie_id+'">'+i.movie_id+'</button></td><td>'+i.status+'</td>/tr>'
    $("#mov2").html($("#mov2").html()+row);
  }
  $.get("/dbMovie/", {}, printCollection);
  $(".umovie").on("click", umovieHandle);
}

function enterCallback(x)
{ 
  if (x["message"] == "0")
  {
    $("#mes").html("User doesn't exist");
  }
  else if (x["message"] == "1")
  {
    $("#mes").html("User doesn't have any current rented checkouts");
  }
  else if (x["message"] == "2")
  {
    $("#mes").html("There is no active account");
  }
  else if (x["message"] == "3")
  {
    $("#mes").html("This user already has 3 movies rented");
  }
  else if (x["message"] == "4")
  {
    $("#mes").html("This user can't rent this movie more than once");
  }
  else if (x["message"] == "5")
  {
    $("#mes").html("This movies has 0 copies left");
  }
  else
  {
    printMovies(x);
  }
}

function enterUserHandle()
{
  $("#email").html("");
  $("#name").html("");
  $("#mov2").html("");
  var email = $("#eU").val();
  out = {email: email};
  $.get("/dbUser/", out, function(x)
  {
    x = JSON.parse(x);
    $("#email").html($("#email").html()+x[0].email);
    $("#name").html($("#name").html()+x[0].fname + " ");
    $("#name").html($("#name").html()+x[0].lname);
  })
  $.get("/dbRent/", out, enterCallback)
}

function movieHandle(e)
{
  var movie = e.target.id;
  out = {movie: movie, action: "rent", email: $("#eU").val()};
  $.post("/dbRent/", out, enterCallback);
}

function umovieHandle(e)
{
  var movie = e.target.id;
  out = {movie: movie, action: "return", email: $("#eU").val()};
  $.post("/dbRent/", out, enterCallback);
}

function printCollection(x) 
{
  $("#mov3").html(" ");
  x = JSON.parse(x);
  for (i of x)
  {
    row = '<tr><td><button class="movie" id="'+i.mname+'">'+i.mname+'</button></td><td>'+i.copies+'</td>/tr>'
    $("#mov3").html($("#mov3").html()+row);
  }
  $(".movie").on("click", movieHandle);
}

$(document).ready(function(){$.get("/dbMovie/", {}, printCollection);});
$("#enterUser").on("click", enterUserHandle);