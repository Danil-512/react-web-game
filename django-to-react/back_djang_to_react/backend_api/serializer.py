from rest_framework import serializers
from .models import *


class MyClass1Serializer(serializers.ModelSerializer):
    class Meta:
        model = MyClass1
        fields = ['type', 'data1', 'data2', 'data3']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Хешируем пароль перед сохранением
        validated_data['password'] = make_password(validated_data['password'])
        user = CustomUser.objects.create(**validated_data)

        # Создаем пустую запись UserInfo
        UserInfo.objects.create(user=user)

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
# class UsersAuthorizationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UsersAuthorization
#         fields = ['userId', 'userPassword']

class UsersListSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='id', read_only=True)
    userLogin = serializers.CharField(source='username')

    class Meta:
        model = CustomUser
        fields = ['userId', 'userLogin']
# class UsersListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UsersList
#         fields = ['userId', 'userLogin']


class UsersInfoSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='user')

    class Meta:
        model = UserInfo
        fields = ['userId', 'first_name', 'second_name', 'email']
        extra_kwargs = {
            'first_name': {'source': 'userFirstName'},
            'second_name': {'source': 'userSecondName'},
            'email': {'source': 'userEmail'}
        }
# class UsersInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UsersInfo
#         fields = ['userId', 'userFirstName', 'userSecondName', 'userEmail']

class AccessTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessTypes
        fields =  ['accessTypeId', 'accessTypeDescr']


class UserAccessSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='user')
    accessTypeId = serializers.PrimaryKeyRelatedField(queryset=AccessTypes.objects.all(), source='access_type')

    class Meta:
        model = CustomUser
        fields = ['userId', 'accessTypeId']
# class UserAccessSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UsersAccess
#         fields =  ['userId', 'accessTypeId']



# # Сериалайзер таблицы связывающей законы и статьи
# class LawsArticlesSerializer(serializers.ModelSerializer):
#     # law_id = serializers.IntegerField(source='law.id', read_only=True)
#     # law_title = serializers.CharField(source='law.title', read_only=True)
#     class Meta:
#         model = LawsArticles
#         fields = ['rec_id', 'law_id', 'article_id']
