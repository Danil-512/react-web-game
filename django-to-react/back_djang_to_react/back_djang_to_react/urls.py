from django.urls import path, include

from backend_api.views import MyClass1View, GetCSRFToken, GetActualUser, CheckSessionView, debug_redis_sessions
from backend_api.views import NewArticle

urlpatterns = [
    path('api/to_react/authorization', include('rest_framework.urls')),
    path('get-csrf/', GetCSRFToken.as_view(), name='get-csrf'),  # Перенесите этот маршрут выше

    path('', MyClass1View.as_view(), name='tttext'),  # Корневой маршрут должен быть последним

    path('get_actual_user/', GetActualUser.as_view(), name='get-actual-user'),

    path('debug/sessions/', debug_redis_sessions, name='debug_sessions'),
    path('laws/<int:p_law_id>/newArticle/', NewArticle.as_view(), name='new_article'),
    path('api/check-session/', CheckSessionView.as_view(), name='check-session'),
    path('check-session/', CheckSessionView.as_view(), name='check-session'),
]