from rest_framework import serializers
from .models import MyClass1, Laws, Articles
from .models import UsersAuthorization
from .models import UsersList
from .models import UsersInfo
from .models import UsersAccess
from .models import AccessTypes
from .models import *


class MyClass1Serializer(serializers.ModelSerializer):
    class Meta:
        model = MyClass1
        fields = ['type', 'data1', 'data2', 'data3']

class UsersAuthorizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersAuthorization
        fields = ['userId', 'userPassword']

class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersList
        fields = ['userId', 'userLogin']

class UsersInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersInfo
        fields = ['userId', 'userFirstName', 'userSecondName', 'userEmail']

class AccessTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessTypes
        fields =  ['accessTypeId', 'accessTypeDescr']

class UserAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersAccess
        fields =  ['userId', 'accessTypeId']


# Сериалайзер таблицы с законами
class LawsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laws
        fields = ['law_id', 'law_number', 'law_title', 'law_date']

# # Сериалайзер таблицы связывающей законы и статьи
# class LawsArticlesSerializer(serializers.ModelSerializer):
#     # law_id = serializers.IntegerField(source='law.id', read_only=True)
#     # law_title = serializers.CharField(source='law.title', read_only=True)
#     class Meta:
#         model = LawsArticles
#         fields = ['rec_id', 'law_id', 'article_id']

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

# Сериалайзер со списком затей и их кратким описанием
class ArticlesShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ('article_number', 'article_title', 'article_descr')

# Сериалайзер пунктов
class ArticleClausesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleClauses
        fields = ('clause_number', 'clause_parent_id', 'clause_text')

