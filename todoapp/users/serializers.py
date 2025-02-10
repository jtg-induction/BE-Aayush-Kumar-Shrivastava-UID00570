from rest_framework import serializers, status
from rest_framework.authtoken.models import Token

from users import models as user_models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.CustomUser
        fields = ['id', 'first_name', 'last_name', 'email']


class UserTodoStatsSerializer(serializers.ModelSerializer):
    completed_count = serializers.IntegerField()
    pending_count = serializers.IntegerField()

    class Meta:
        model = user_models.CustomUser
        fields = [
            'id', 'first_name', 'last_name', 'email', 
            'completed_count', 'pending_count'
        ]


class PendingTodosSerializer(serializers.ModelSerializer):
    pending_count = serializers.IntegerField()

    class Meta:
        model = user_models.CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'pending_count']


class UserWiseProjectStatusSerializer(serializers.ModelSerializer):
    to_do_projects = serializers.ListField()
    in_progress_projects = serializers.ListField()
    completed_projects = serializers.ListField()

    class Meta:
        model = user_models.CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'to_do_projects', 
            'in_progress_projects', 'completed_projects'
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = user_models.CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'password', 'date_joined'
        ]
        read_only_fields = ['date_joined']

    def validate_email(self, value):
        if user_models.CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                {"email":"Email already exists"}, 
                code=status.HTTP_201_CREATED
            )

        return value

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

    def create(self, validated_data):
        user = user_models.CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )

        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        token, _ = Token.objects.get_or_create(user=instance)
        representation['token'] = token.key

        return representation
