from django.db import models

# Create your models here.
class MyClass1(models.Model):
    type = models.CharField(max_length=100)
    data1 = models.CharField(max_length=300)
    data2 = models.CharField(max_length=300)
    data3 = models.CharField(max_length=300)

# Model for authorization
class AuthorizationModel(models.Model):
    user_id = models.CharField(max_length=20)
    user_login = models.CharField(max_length=100)
    user_password = models.CharField(max_length=100)