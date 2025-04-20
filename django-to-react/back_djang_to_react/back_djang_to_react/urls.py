"""
URL configuration for back_djang_to_react project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.urls import re_path as url
from backend_api.views import *
from backend_api.functions_to_auth_and_reg import  add_new_user, access_type_create

#from ..backend_api.views import  LawListView, LawArticlesView



urlpatterns = [
    path('admin/', admin.site.urls),
    # Строка для подключения авторизации на основе сессии
    path('api/to_react/authorization', include('rest_framework.urls')),
    path('', MyClass1View.as_view(), name='tttext'),


    #path('laws/', LawListView.as_view(), name='laws-list'),
    path('laws/', LawListView.as_view(), name='laws-list'),
    #path('laws/<int:law_id>/articles/', LawStView.as_view(), name='law-st'),


    path('laws/<int:law_id>/<str:str2>/', LawArticleDetailView.as_view(), name='law-st'),
    path('laws/<int:law_id>/articles', LawArticlesView.as_view(), name='law-st-articles'),
    path('laws/<int:law_id>', LawArticlesView.as_view(), name='law-st-articles'),





    # path('laws/<int:law_id>/', LawStView.as_view(), name='law-st'),
    # path('laws/<int:law_id>/articles/', LawArticlesView.as_view(), name='law-st-articles'),


    #path('api/laws/<int:law_id>/articles/', LawArticlesView.as_view()),  # Для фронтенда через прокси
    #path('api/laws/', LawListView.as_view(), name='laws-list'),
    #path('api/laws/<int:law_id>/articles/', LawArticlesView.as_view(), name='law-articles'),
]
