from django.urls import path
from laws.views import LawsListView, LawArticlesListView, ArticleTextListView, NewArticle

urlpatterns = [
    path('rest_api/laws',                                    LawsListView.as_view(),        name='laws-list'),
    path('rest_api/laws/',                                   LawsListView.as_view(),        name='laws-list'),

    path('rest_api/laws/<int:p_law_id>/',                    LawArticlesListView.as_view(), name='law-articles-list'),

    path('rest_api/laws/<int:p_law_id>/<int:p_article_id>/', ArticleTextListView.as_view(), name='article_text'),

    path('rest_api/laws/<int:p_law_id>/newArticle/',         NewArticle.as_view(),          name='new_article')
]
