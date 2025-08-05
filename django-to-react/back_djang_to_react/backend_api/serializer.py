from rest_framework import serializers
from .models import *


# Сериалайзер для получаемых при регистрации и авторизации логине и пароле
class UserLoginPasswordSerializer(serializers.Serializer):
    userLogin    = serializers.CharField()
    userPassword = serializers.CharField()


class UsersListSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='id', read_only=True)
    userLogin = serializers.CharField(source='username')
    #
    class Meta:
        model = CustomUser
        fields = ['userId', 'userLogin']


class UsersInfoSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='user')
    #
    class Meta:
        model = UserInfo
        fields = ['userId', 'first_name', 'second_name', 'email']
        extra_kwargs = {
            'first_name': {'source': 'userFirstName'},
            'second_name': {'source': 'userSecondName'},
            'email': {'source': 'userEmail'}
        }


class AccessTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessTypes
        fields =  ['accessTypeId', 'accessTypeDescr']


class UserAccessSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='user')
    accessTypeId = serializers.PrimaryKeyRelatedField(queryset=AccessTypes.objects.all(), source='access_type')
    #
    class Meta:
        model = CustomUser
        fields = ['userId', 'accessTypeId']
