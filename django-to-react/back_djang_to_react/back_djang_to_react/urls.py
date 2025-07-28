from django.urls import path, include

from backend_api.views import MyClass1View, GetCSRFToken, GetActualUser, CheckSessionView, debug_redis_sessions
from backend_api.views import NewArticle

from .yasg import urlpatterns as doc_urls

urlpatterns = [
    #
    # path('api/to_react/authorization', include('rest_framework.urls')),
    #
    # Получение нового токена сессии
    path('get-csrf/', GetCSRFToken.as_view(), name='get-csrf'),
    #
    # Авторизация и регистрация (Нужно разделить на отдельные адреса и функции)
    path('', MyClass1View.as_view(), name='tttext'),  # Корневой маршрут должен быть последним
    #
    # Получение информации об актуальном авторизированном пользователе
    path('get_actual_user/', GetActualUser.as_view(), name='get-actual-user'),
    #
    # Информация о сессиях в редисе
    path('debug/sessions/', debug_redis_sessions, name='debug_sessions'),
    #
    # Добавление новой статьи к закону
    path('laws/<int:p_law_id>/newArticle/', NewArticle.as_view(), name='new_article'),
    #
    # Получение информации о текущей сессии
    path('api/check-session/', CheckSessionView.as_view(), name='check-session'),
    path('check-session/', CheckSessionView.as_view(), name='check-session'),
]

# Добавление адресов с документацией
urlpatterns += doc_urls