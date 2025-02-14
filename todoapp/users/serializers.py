from django.contrib.auth import authenticate

from rest_framework import serializers, status
from rest_framework.authtoken.models import Token

from users import models as user_models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.CustomUser
        model = user_models.CustomUser
        fields = ['id', 'first_name', 'last_name', 'email']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()
    
    class Meta:
        model = user_models.CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'password', 'date_joined', 'token'
        ]
        read_only_fields = ['date_joined', 'token']
        
    def get_token(self, instance): 
        token, _ = Token.objects.get_or_create(user=instance)
        
        return token.key
        
    def validate(self, attrs):
        confirm_password = self.context['request'].data.get(
            'confirm_password', None)
        if not confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "This field is required."}
            )

        if attrs["password"] != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}, 
                code=status.HTTP_400_BAD_REQUEST
            )

        return attrs


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError({"error": "Invalid email or password."}, code=status.HTTP_400_BAD_REQUEST)

        return attrs
    