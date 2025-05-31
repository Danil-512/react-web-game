from django.contrib import admin
from django.urls import path, include

from django.urls import re_path as url
from backend_api.views import MyClass1View, LawsListView, LawArticlesListView, ArticleTextListView, NewArticle, GetCSRFToken, GetActualUser, CheckSessionView, debug_redis_sessions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/to_react/authorization', include('rest_framework.urls')),
    path('get-csrf/', GetCSRFToken.as_view(), name='get-csrf'),  # Перенесите этот маршрут выше
    #path('api/', include('backend_api.urls')),  # Перенесите этот маршрут выше

    path('', MyClass1View.as_view(), name='tttext'),  # Корневой маршрут должен быть последним

    path('get_actual_user/', GetActualUser.as_view(), name='get-actual-user'),

    path('debug/sessions/', debug_redis_sessions, name='debug_sessions'),

    path('check-session/', CheckSessionView.as_view(), name='check-session'),

    path('laws/', LawsListView.as_view(), name='laws-list'),
    path('laws/<int:p_law_id>/', LawArticlesListView.as_view(), name='law-articles'),
    path('laws/<int:p_law_id>/<int:p_article_id>/', ArticleTextListView.as_view(), name='article_text'),
    path('laws/<int:p_law_id>/newArticle/', NewArticle.as_view(), name='new_article')
]