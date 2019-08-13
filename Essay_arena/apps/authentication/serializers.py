from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User

class ClientRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
 
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']
 
    def create(self, validated_data):
        return User.objects.create_client(**validated_data)
 
class WriterRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
 
    class Meta:
        model = User
        print(model, 'modelize')
        fields = ['id', 'email', 'username', 'password']
 
    def create(self, validated_data):
        print(validated_data, "thereh")
        return User.objects.create_writer(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    is_writer = serializers.BooleanField(read_only=True)
    is_client = serializers.BooleanField(read_only=True)
 
    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(username=email, password=password)
 
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
 
        try:
            userObj = User.objects.get(email=user.email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )        

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
 
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token,
            'is_writer': user.is_writer,
            'is_client': user.is_client
        }