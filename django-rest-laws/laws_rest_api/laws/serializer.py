from rest_framework import serializers

from .models import Laws, Articles, ArticleClauses, RespToArticles


# Сериалайзер таблицы с законами
class LawsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laws
        fields = ['law_id', 'law_number', 'law_title', 'law_date']


# Сериалайзер таблицы со статьями закона
class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ('article_id', 'article_parent_id', 'article_number', 'article_title', 'article_file_path')

# Сериалайзер со списком законов и их кратким описанием
class LawsShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laws
        fields = ('law_id', 'law_title')

# Сериалайзер со списком статей и их кратким описанием
class ArticlesShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ('article_id', 'article_number', 'article_title', 'article_descr')

# Сериалайзер со списком статей и их типами ответсвенности за нарушение
class ArticlesResponsibilitys(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ('article_number', 'article_title', 'article_descr')


# Сериалайзер пунктов
class ArticleClausesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleClauses
        fields = ('clause_number', 'clause_parent_id', 'clause_text')

# Сериалайзер ответсвенности за статьи
class RespToArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespToArticles
        fields = (
            'resp_article_record_id'
            ,'resp_article_id'
            ,'resp_first_type'
            ,'resp_second_type'
            ,'resp_third_type'
            ,'resp_fourth_type'
            ,'resp_another_type'
        )