from rest_framework import serializers
from .models import MyClass1
from .models import AuthorizationModel

class MyClass1Serializer(serializers.ModelSerializer):
    class Meta:
        model = MyClass1
        fields = ['type', 'data1', 'data2', 'data3']

class AuthorizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorizationModel
        fields = ['user_id', 'user_login', 'user_password']