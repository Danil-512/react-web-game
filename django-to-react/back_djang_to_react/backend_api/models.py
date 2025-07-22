from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager
# Модели в django - таблицы в базе данных
# Поля модели - атрибуты отношения в базе данных (столбцы таблицы)

# Base input data model
class MyClass1(models.Model):
    # Базовая модель для обработки гет и пут запросов
    type           = models.CharField(max_length=100)
    data1          = models.CharField(max_length=300)
    data2          = models.CharField(max_length=300)
    data3          = models.CharField(max_length=300)

# Model for types access rights
class AccessTypes(models.Model):
    # Модель хранит виды доступа пользователей
    access_type_id    = models.IntegerField(blank=False, primary_key=True)
    access_type_descr = models.CharField(max_length=100, blank=False)
    #
    # Строковое представление модели для отображения в админ панели и логах
    def __str__(self):
        return f'{self.access_type_id} {self.access_type_descr}'
    #
    # Название таблицы в базе данных - типы доступа пользователей
    class Meta:
        db_table = 'access_types'

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        # Удаляем поля, которых нет в модели
        extra_fields.pop('email', None)
        extra_fields.pop('is_staff', None)
        extra_fields.pop('is_superuser', None)

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('access_type_id', 1)  # Или ваш ID для суперпользователя

        return self.create_user(username, password, **extra_fields)

# Класс для настройки работы базового механизма авторизации django через кастомную модель со своей таблицей
class CustomUser(AbstractUser):
    # Добавляемые атрибуты - все остальные есть в таблице по умолчанию
    access_type = models.ForeignKey(AccessTypes, on_delete=models.SET_DEFAULT, default=1)
    #
    # Отключение лишних атрибутов базовой модели (они перенесены в отдельную таблицу)
    is_superuser = None
    first_name   = None
    last_name    = None
    email        = None
    is_staff     = None
    #
    ## Поля по умолчанию:
    ## id          - int8         - NOT NULL, PRIMARY KEY
    ## username    - varchar(150) - NOT NULL, UNIQUE
    ## password    - varchar(128) - NOT NULL
    ## is_active   - bool         - NOT NULL
    ## access_type - int4         - NOT NULL
    ## date_joined - timestamptz  - NOT NULL
    ## last_login  - timestamptz
    #
    # Используем кастомный менеджер
    objects = CustomUserManager()
    #
    # Название таблицы в базе данных - список пользователей
    class Meta:
        db_table = 'users_list'
    #
    # Убираем ненужные поля из REQUIRED_FIELDS
    REQUIRED_FIELDS = []


# Модель с дополнительной информацией о пользователе
class UserInfo(models.Model):
    user        = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name  = models.CharField(max_length=100, blank=True)
    second_name = models.CharField(max_length=100, blank=True)
    email       = models.CharField(max_length=100, blank=True)
    #
    # Название таблицы в базе данных - информация о пользователе
    class Meta:
        db_table = 'users_info'