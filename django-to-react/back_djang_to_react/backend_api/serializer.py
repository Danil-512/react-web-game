from rest_framework import serializers
from .models import MyClass1, LawArticle, Law
from .models import UsersAuthorization
from .models import UsersList
from .models import UsersInfo
from .models import UsersAccess
from .models import AccessTypes


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


class LawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Law
        fields = ['id', 'title', 'date', 'number']


# class LawArticleSerializer(serializers.ModelSerializer):
#     parent_id = serializers.IntegerField(source='law.id', read_only=True)
#
#     class Meta:
#         model = LawArticle
#         fields = ['id', 'title', 'date', 'text', 'parent_id']

class LawArticleSerializer(serializers.ModelSerializer):
    law_id = serializers.IntegerField(source='law.id', read_only=True)
    law_title = serializers.CharField(source='law.title', read_only=True)

    class Meta:
        model = LawArticle
        fields = ['id', 'title', 'date', 'text', 'law_id', 'law_title']

class LawArticleShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawArticle
        fields = ('id', 'title', 'law_id')

class LawArticleShortSerializer2(serializers.ModelSerializer):
    class Meta:
        model = LawArticle
        fields = ('id', 'title')  # Убедитесь, что эти поля существуют в модели