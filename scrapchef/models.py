from django.db import models

# Create your models here.

class User(models.Model):
    UserName = models.CharField(max_length=64)
    Password = models.CharField(max_length=64)
    Occupation = models.CharField(max_length=64)
    ProfilePhoto = models.CharField(max_length=255)

    def __str__(self):
        return self.UserName
