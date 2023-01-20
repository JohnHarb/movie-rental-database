from django.db import models
  
class User(models.Model):
  fname = models.CharField(max_length=20)
  lname = models.CharField(max_length=20)
  email = models.CharField(max_length=30, primary_key = True)

class Movie(models.Model):
  mname = models.CharField(max_length=20, primary_key = True)
  copies = models.IntegerField()

class Checkout(models.Model):
  status = models.CharField(max_length=20)
  movie = models.ForeignKey(Movie, on_delete=models.CASCADE, default="default")
  user = models.ForeignKey(User, on_delete=models.CASCADE, default="default")