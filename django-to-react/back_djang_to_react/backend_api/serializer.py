from rest_framework import serializers
from .models import MyClass1
from .models import UsersAuthorization
from .models import UsersList
from .models import UsersInfo


class MyClass1Serializer(serializers.ModelSerializer):
    class Meta:
        model = MyClass1
        fields = ['type', 'data1', 'data2', 'data3']

class UsersAuthorizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersAuthorization
        fields = ['user_id', 'user_login', 'user_password']

class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersList
        fields = ['user_id', 'user_login']

class UsersInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersInfo
        fields = ['user_id', 'user_first_name', 'user_second_name', 'user_email']