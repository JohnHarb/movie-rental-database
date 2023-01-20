from django.views import View 
from django.http import JsonResponse
from django.shortcuts import render
from mysite.models import Movie, User, Checkout
import json

class Home(View):
  def get(self, request):
   return render(request,"home.html",{})
    
class accountHandle(View):
  def get(self, request):
    return render(request,"account.html",{})
    
class movieHandle(View):
  def get(self, request):
    return render(request,"movie.html",{})

class rentHandle(View):
  def get(self, request):
    return render(request,"rent.html",{})

class dbUserHandle(View):
  def get(self, request):
    email = request.GET.get("email",None)
    if len(User.objects.filter(email=email)) == 0:
      return JsonResponse({"message": "0"});
    ret = User.objects.filter(email=email).values()
    print(list(ret))
    return JsonResponse(json.dumps(list(ret)),safe=False)
      
  def post(self, request):
    message = ""
    fname = ""
    lname = ""
    email = ""
    if request.POST["fname"].isspace() or request.POST["lname"].isspace() or request.POST["email"].isspace():
      message = "some fields were empty"
    elif len(User.objects.filter(email=request.POST["email"])) > 0:
      message = "account email is already used"
    else:
      fname = request.POST["fname"]
      lname = request.POST["lname"]
      email = request.POST["email"]
      message = "successfully created account"
      newUser = User(fname=fname, lname=lname, email=email)
      newUser.save()
    return render(request,"account.html",{"message": message, "fname": fname,"lname": lname, "email": email})

class dbMovieHandle(View):
  def get(self, request):
    ret = Movie.objects.all().values()
    return JsonResponse(json.dumps(list(ret)),safe=False)
    
  def post(self, request):
    
    movie = request.POST.get("movie",None)
    if movie.isspace():
      return JsonResponse({"message": "0"});
      
    action = request.POST.get("action",None) 
    if action == "new":
      if len(Movie.objects.filter(mname=movie)) > 0:
        return JsonResponse({"message": "0"});
      newMovie = Movie(mname=movie, copies=1)
      newMovie.save()
    elif action == "add":
      existmovie = Movie.objects.filter(mname=movie)[0]
      existmovie.copies += 1
      existmovie.save()
    else:
      existmovie = Movie.objects.filter(mname=movie)[0]
      if(existmovie.copies > 0):
        existmovie.copies -= 1
      else:
        existmovie.copies = 0
      existmovie.save()
      
    ret = Movie.objects.all().values()
    return JsonResponse(json.dumps(list(ret)),safe=False)
  
class dbRentHandle(View):
  def get(self, request):
    email = request.GET.get("email",None)
    if len(User.objects.filter(email=email)) == 0:
      return JsonResponse({"message": "0"});
    myUser = User.objects.filter(email=email)[0]
    if len(Checkout.objects.filter(user=myUser, status="rented")) == 0:
      return JsonResponse({"message": "1"});
    ret = Checkout.objects.filter(user=myUser, status="rented").values()
    return JsonResponse(json.dumps(list(ret)),safe=False)
  def post(self, request):
    email = request.POST.get("email",None)
    action = request.POST.get("action",None)
    movie = request.POST.get("movie",None)
    if not(email):
      return JsonResponse({"message": "2"});
    uMovie = Movie.objects.filter(mname=movie)[0]
    myUser = User.objects.filter(email=email)[0]
    if action == "rent":
      if uMovie.copies == 0:
        return JsonResponse({"message": "5"});
      if len(Checkout.objects.filter(user=myUser, movie=uMovie, status ="rented")) > 0:
        return JsonResponse({"message": "4"});
      if len(Checkout.objects.filter(user=myUser, status = "rented")) >= 3:
        return JsonResponse({"message": "3"});
      uMovie.copies -= 1
      uMovie.save()
      if len(Checkout.objects.filter(user=myUser, movie=uMovie, status ="returned")) > 0:
        uCheck = Checkout.objects.filter(user=myUser, movie=uMovie, status ="returned")[0]
        uCheck.status = "rented"
        uCheck.save()
      else:
        uCheck = Checkout(user=myUser, movie=uMovie, status = "rented")
        uCheck.save()
    else:
      uMovie.copies += 1
      uMovie.save()
      uCheck = Checkout.objects.filter(user=myUser, movie=uMovie, status ="rented")[0]
      uCheck.status = "returned"
      uCheck.save()
    ret = Checkout.objects.filter(user=myUser, status="rented").values()
    print(list(ret))
    return JsonResponse(json.dumps(list(ret)),safe=False)