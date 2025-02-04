from rest_framework import serializers
from rest_framework.authtoken.models import Token

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email']


class UserTodoStatsSerializer(serializers.ModelSerializer):
    completed_count = serializers.IntegerField()
    pending_count = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name',
                  'email', 'completed_count', 'pending_count']


class PendingTodosSerializer(serializers.ModelSerializer):
    pending_count = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'pending_count']


class UserWiseProjectStatusSerializer(serializers.ModelSerializer):
    to_do_projects = serializers.ListField()
    in_progress_projects = serializers.ListField()
    completed_projects = serializers.ListField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'to_do_projects',
                  'in_progress_projects', 'completed_projects']


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name',
                  'email', 'password', 'date_joined']
        read_only_fields = ['date_joined']
        write_only_fields = ['password']

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists.")

        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
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
