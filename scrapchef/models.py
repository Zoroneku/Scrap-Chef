from django.db import models

# Create your models here.

class User(models.Model):
    UserName = models.CharField(max_length=64)
    Password = models.CharField(max_length=64)
    Occupation = models.CharField(max_length=64)
    ProfilePhoto = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.UserName
    
class Post(models.Model):
    PostID = models.CharField(max_length=64, unique=True)
    Media = models.CharField(max_length=255)
    Caption = models.CharField(max_length=255)

    def __str__(self):
        return self.Caption
    
class Review(models.Model):
    ReviewID = models.CharField(max_length=64, unique=True)
    Taste = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  
    Struggle = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  
    Preparation = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  

    def __str__(self):
        return f"Review {self.ReviewID}"
    
class List(models.Model):
    Title = models.CharField(max_length=64)
    Description = models.TextField()
    PostID = models.CharField(max_length=64)

    def __str__(self):
        return self.Title

