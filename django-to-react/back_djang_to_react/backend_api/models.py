from django.db import models

# Модели в django - таблицы в базе данных
# Поля модели - атрибуты отношения в базе данных (столбцы таблицы)

# Model fo list users
class UsersList(models.Model):
    userId = models.IntegerField(blank=False)
    userLogin = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f'{self.userId} {self.userLogin}'


# Model fo users authorization data
class UsersAuthorization(models.Model):
    userId = models.IntegerField(blank=False)
    userLogin = models.CharField(max_length=100, blank=False)
    userPassword = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f'{self.userId} {self.userLogin}'


# Model fo users data
class UsersInfo(models.Model):
    userId = models.IntegerField(blank=False)
    userFirstName = models.CharField(max_length=100, blank=True)
    userSecondName = models.CharField(max_length=100, blank=True)
    userEmail = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.userId)

# Create your models here.
class MyClass1(models.Model):
    type = models.CharField(max_length=100)
    data1 = models.CharField(max_length=300)
    data2 = models.CharField(max_length=300)
    data3 = models.CharField(max_length=300)