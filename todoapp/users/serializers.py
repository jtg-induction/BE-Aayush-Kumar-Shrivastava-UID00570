from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
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
        fields = [
            'id', 'first_name', 'last_name',
            'email', 'completed_count', 'pending_count'
        ]


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
        fields = [
            'first_name', 'last_name', 'email', 'to_do_projects',
            'in_progress_projects', 'completed_projects'
        ]
