from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
# Модели в django - таблицы в базе данных
# Поля модели - атрибуты отношения в базе данных (столбцы таблицы)

# Base input data model
class MyClass2(models.Model):
    type           = models.CharField(max_length=100)
    data1          = models.CharField(max_length=300)
    data2          = models.CharField(max_length=300)
    data3          = models.CharField(max_length=300)

# Base input data model
class MyClass1(models.Model):
    type           = models.CharField(max_length=100)
    data1          = models.CharField(max_length=300)
    data2          = models.CharField(max_length=300)
    data3          = models.CharField(max_length=300)

# Model for types access rights
class AccessTypes(models.Model):
    access_type_id    = models.IntegerField(blank=False, primary_key=True)
    access_type_descr = models.CharField(max_length=100, blank=False)
    def __str__(self):
        return f'{self.access_type_id} {self.access_type_descr}'
    class Meta:
        db_table = 'access_types'


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username must be set')

        access_type = extra_fields.pop('access_type', None) or AccessTypes.objects.get(accessTypeId=1)

        user = self.model(
            username=username,
            access_type=access_type,
            **extra_fields
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    access_type = models.ForeignKey(AccessTypes, on_delete=models.SET_DEFAULT, default=1)

    class Meta:
        db_table = 'users_list'


class UserInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100, blank=True)
    second_name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'users_info'


# # More information about user
# class UserInfo(models.Model):
#     first_name = models.CharField(max_length=100, blank=True)
#     second_name = models.CharField(max_length=100, blank=True)
#     email = models.CharField(max_length=100, blank=True)
#
#     def __str__(self):
#         return f'{self.first_name} {self.second_name} ({self.email})'
#
# # Model for list users
# class UsersList(models.Model):
#     userId         = models.AutoField(             blank=False, primary_key=True, )
#     userLogin      = models.CharField(max_length=100, blank=False, unique=True)
#
#     def __str__(self):
#         return f'{self.userId} {self.userLogin}'
#
#
# # Model for users authorization data
# class UsersAuthorization(models.Model):
#     userId         = models.ForeignKey(UsersList, to_field='userId', on_delete=models.CASCADE)
#     userPassword   = models.CharField(max_length=100, blank=False)
#
#     def __str__(self):
#         return f'{self.userId} {self.userPassword}'
#
#
# # Model for users data
# class UsersInfo(models.Model):
#     userId         = models.ForeignKey(UsersList,   to_field='userId', on_delete=models.CASCADE)
#     userFirstName  = models.CharField(max_length=100, blank=True)
#     userSecondName = models.CharField(max_length=100, blank=True)
#     userEmail      = models.CharField(max_length=100, blank=True)
#
#     def __str__(self):
#         return str(f'{self.userId} {self.userEmail} {self.userFirstName} {self.userSecondName}')
#
# # Model for users access rights information
# class UsersAccess(models.Model):
#     userId         = models.ForeignKey(UsersList,     to_field='userId',               on_delete=models.CASCADE)
#     accessTypeId   = models.ForeignKey(AccessTypes, default=0, to_field='accessTypeId', on_delete=models.SET_DEFAULT)
#     def __str__(self):
#         return str(f'{self.userId} {self.accessTypeId}')




# Таблица с законами
class Laws(models.Model):
    law_id     = models.IntegerField(primary_key=True)
    law_number = models.CharField(blank=False, max_length=20, verbose_name="Номер закона", unique=True)
    law_title  = models.CharField(blank=False, max_length=400, verbose_name="Название закона")
    law_date   = models.DateField(verbose_name="Дата принятия")

    def __str__(self):
        return f"{self.law_number} - {self.law_title}"

# Таблица со статьями закона
class Articles(models.Model):
    article_id = models.AutoField(primary_key=True)
    article_parent_id = models.ForeignKey(Laws, to_field='law_id', on_delete=models.CASCADE, blank=False, default=0)
    article_number = models.IntegerField(blank=False)
    article_title = models.CharField(blank=False, max_length=100)
    article_descr = models.CharField(blank=False, max_length=400, default='')

# Пункты статьи
class ArticleClauses(models.Model):
    clause_id = models.AutoField(primary_key=True)
    clause_number = models.IntegerField(blank=False, default=0)
    clause_parent_id = models.ForeignKey(Articles, to_field='article_id', on_delete=models.CASCADE, blank=False, default=0)
    clause_text = models.CharField(blank=False, max_length=2000)

# Таблица с видами ответсвенности
class Responsibilitys(models.Model):
    responsibility_id = models.IntegerField(primary_key=True)
    responsibility_type = models.CharField(blank=False, max_length=50)

class RespToLaws(models.Model):
    resp_law_record_id = models.IntegerField(primary_key=True)
    resp_law_id = models.ForeignKey(Laws, to_field='law_id', blank=False, on_delete=models.CASCADE)
    resp_first_type = models.IntegerField(blank=False, default=0)
    resp_second_type = models.IntegerField(blank=False, default=0)
    resp_third_type = models.IntegerField(blank=False, default=0)
    resp_fourth_type = models.IntegerField(blank=False, default=0)
    resp_another_type = models.IntegerField(blank=False, default=0)
    resp_none_type = models.IntegerField(blank=False, default=0)


class RespToArticles(models.Model):
    resp_article_record_id = models.AutoField(primary_key=True)
    resp_article_id = models.ForeignKey(Articles, to_field='article_id', blank=False, on_delete=models.CASCADE)
    resp_first_type = models.IntegerField(blank=False, default=0)
    resp_second_type = models.IntegerField(blank=False, default=0)
    resp_third_type = models.IntegerField(blank=False, default=0)
    resp_fourth_type = models.IntegerField(blank=False, default=0)
    resp_another_type = models.IntegerField(blank=False, default=0)

# # Таблица для связывания законов и статей
# class LawsArticles(models.Model):
#     rec_id = models.AutoField(primary_key=True)
#     law_id = models.ForeignKey(Laws, to_field='law_id', on_delete=models.CASCADE, blank=False)
#     article_id = models.ForeignKey(Articles, to_field='article_id', on_delete=models.CASCADE, blank=False)
#

