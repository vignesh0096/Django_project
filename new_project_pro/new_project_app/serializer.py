from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CustomUserSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField()
    phone_number = serializers.IntegerField()
    email = serializers.EmailField()
    role = serializers.CharField()


class PermissionGeneratorCustomSerializer(serializers.Serializer):
    model_name = serializers.CharField()


class PermissionGeneratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissiongenerator
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'


class RoleSerializerCustom(serializers.Serializer):
    ROLES = {
        ('ADMIN', 'ADMIN'),
        ('TL', 'TL'),
        ('USER', 'USER')
    }
    role = serializers.ChoiceField(choices=ROLES)



