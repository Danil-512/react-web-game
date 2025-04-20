from django.db import models

# Модели в django - таблицы в базе данных
# Поля модели - атрибуты отношения в базе данных (столбцы таблицы)

# Base input data model
class MyClass1(models.Model):
    type           = models.CharField(max_length=100)
    data1          = models.CharField(max_length=300)
    data2          = models.CharField(max_length=300)
    data3          = models.CharField(max_length=300)

# Model for types access rights
class AccessTypes(models.Model):
    accessTypeId    = models.IntegerField(blank=False, primary_key=True)
    accessTypeDescr = models.CharField(max_length=100, blank=False)
    def __str__(self):
        return f'{self.accessTypeId} {self.accessTypeDescr}'

# Model for list users
class UsersList(models.Model):
    userId         = models.AutoField(             blank=False, primary_key=True, )
    userLogin      = models.CharField(max_length=100, blank=False, unique=True)

    def __str__(self):
        return f'{self.userId} {self.userLogin}'


# Model for users authorization data
class UsersAuthorization(models.Model):
    userId         = models.ForeignKey(UsersList, to_field='userId', on_delete=models.CASCADE)
    userPassword   = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f'{self.userId} {self.userPassword}'


# Model for users data
class UsersInfo(models.Model):
    userId         = models.ForeignKey(UsersList,   to_field='userId', on_delete=models.CASCADE)
    userFirstName  = models.CharField(max_length=100, blank=True)
    userSecondName = models.CharField(max_length=100, blank=True)
    userEmail      = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(f'{self.userId} {self.userEmail} {self.userFirstName} {self.userSecondName}')

# Model for users access rights information
class UsersAccess(models.Model):
    userId         = models.ForeignKey(UsersList,     to_field='userId',               on_delete=models.CASCADE)
    accessTypeId   = models.ForeignKey(AccessTypes, default=0, to_field='accessTypeId', on_delete=models.SET_DEFAULT)
    def __str__(self):
        return str(f'{self.userId} {self.accessTypeId}')


# Навайбил
class Law(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название закона")
    date = models.DateField(verbose_name="Дата принятия")
    number = models.CharField(max_length=50, verbose_name="Номер закона")

    def __str__(self):
        return f"{self.number} - {self.title}"

class LawArticle(models.Model):
    law = models.ForeignKey(Law, on_delete=models.CASCADE, related_name='articles', verbose_name="Родительский закон")
    title = models.CharField(max_length=255, verbose_name="Название статьи")
    date = models.DateField(verbose_name="Дата добавления")
    text = models.TextField(verbose_name="Текст статьи")

    def __str__(self):
        return f"{self.law.number} - {self.title}"
