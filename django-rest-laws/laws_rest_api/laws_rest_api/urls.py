from django.urls import path
from laws.views import HealthCheck, LawsListView, LawArticlesListView, ArticleTextListView, NewArticle
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('rest_api/laws/',                                   LawsListView.as_view(),        name='laws-list'),

    path('rest_api/laws/<int:p_law_id>/',                    LawArticlesListView.as_view(), name='articles-list'),

    # Проверка статуса работоспособности для докер компоуза
    path('health2/', HealthCheck.as_view(), name='health'),

    path('rest_api/laws/<int:p_law_id>/<int:p_article_id>/', ArticleTextListView.as_view(), name='article_text'),

    path('rest_api/laws/<int:p_law_id>/newArticle/',         NewArticle.as_view(),          name='new_article')
]

# К уже имеющимся адресам, добавить адреса документации
urlpatterns += doc_urls