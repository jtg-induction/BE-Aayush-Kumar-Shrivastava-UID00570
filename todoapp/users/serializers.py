from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from rest_framework import serializers, status
from rest_framework.authtoken.models import Token

from users import models as user_models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.CustomUser
        fields = ['id', 'first_name', 'last_name', 'email']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()
    
    class Meta:
        model = user_models.CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'password', 'date_joined', 'token', 'confirm_password'
        ]
        read_only_fields = ['date_joined', 'token']
        
    def get_token(self, instance): 
        token, _ = Token.objects.get_or_create(user=instance)
        
        return token.key
        
    def validate(self, attrs):
        if attrs["password"] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}, 
                code=status.HTTP_400_BAD_REQUEST
            )
            
        attrs['password'] = make_password(attrs['password'])
        attrs.pop('confirm_password')
        
        return attrs


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['email'], password=attrs['password'])

        if user is None:
            raise serializers.ValidationError(
                {"error": "Invalid email or password."},
                code=status.HTTP_400_BAD_REQUEST
            )
        
        attrs['user'] = user
        return attrs
