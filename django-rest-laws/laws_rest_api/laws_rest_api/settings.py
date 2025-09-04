from pathlib import Path
import environ
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/


# Инициализация django-environ
env = environ.Env(
    DEBUG=(bool, False),
    # Тут можно указывать дефолтные значения
    DJANGO_MAIN_SECRET_KEY=(str, ''),
    DJANGO_LAWS_SERVER_PATH=(str, ''),
    FRONT_SERVER_PATH=(str, ''),
    MAIN_DATABASE_HOST=(str, ''),
    MAIN_DATABASE_PORT=(int, None),
    MAIN_DATABASE_USER=(str, ''),
    MAIN_DATABASE_PASSWORD=(str, ''),
    MAIN_DATABASE_LAWS_NAME=(str, ''),
    REDIS_HOST=(str, ''),
    REDIS_PASSWORD=(str, ''),
    REDIS_PORT=(int, None),
)
#
# Чтение файла .env, который находиться на директорию выше чем базовая директория проекта
environ.Env.read_env(os.path.join(BASE_DIR, '../.env'))
#
# Создание словаря со всеми нужными переменными
env_dict = {
    'FRONT_SERVER_PATH'           : env('FRONT_SERVER_PATH'),
    'DJANGO_MAIN_SERVER_PATH'     : env('VITE_MAIN_BACK_SERVER_PATH'),
    'DJANGO_LAWS_SERVER_PATH'     : env('VITE_LAWS_BACK_SERVER_PATH'),
    'SECRET_KEY'                  : env('DJANGO_LAWS_SECRET_KEY'),
    'MAIN_DATABASE_HOST'          : env('MAIN_DATABASE_HOST'),
    'MAIN_DATABASE_PORT'          : env('MAIN_DATABASE_PORT'),
    'MAIN_DATABASE_INTERNAL_PORT' : env('MAIN_DATABASE_INTERNAL_PORT'),
    'MAIN_DATABASE_USER'          : env('MAIN_DATABASE_USER'),
    'MAIN_DATABASE_PASSWORD'      : env('MAIN_DATABASE_PASSWORD'),
    'MAIN_DATABASE_LAWS_NAME'     : env('MAIN_DATABASE_LAWS_NAME'),
    'DOCKER_COMPOSE'              : env('DOCKER_COMPOSE'),
}
#
# # Проверка получения переменных окружения
# print('/---------------------------------------')
# print('Проверка получения переменных окружения')
# for key, value in env_dict.items():
#     print(f'key is {key}, value is {value}')
# print('---------------------------------------/')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env_dict['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Мое приложение
    'laws.apps.LawsConfig',
    # Расширение для ведения документации
    'drf_yasg',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    env_dict['FRONT_SERVER_PATH'],
    env_dict['DJANGO_MAIN_SERVER_PATH'],
    env_dict['DJANGO_LAWS_SERVER_PATH'],
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_HEADERS = True

ROOT_URLCONF = 'laws_rest_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'laws_rest_api.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Если приложение запускается на сервере через докер компоуз - то порт 5432, если извне то 5433
if env_dict['DOCKER_COMPOSE'] == 'true':
    DB_PORT = env_dict['MAIN_DATABASE_INTERNAL_PORT']
else:
    DB_PORT = env_dict['MAIN_DATABASE_PORT']


DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.postgresql',
        "HOST"    : env_dict['MAIN_DATABASE_HOST'],
        "PORT"    : DB_PORT,
        "USER"    : env_dict['MAIN_DATABASE_USER'],
        "PASSWORD": env_dict['MAIN_DATABASE_PASSWORD'],
        "NAME"    : env_dict['MAIN_DATABASE_LAWS_NAME'],
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'