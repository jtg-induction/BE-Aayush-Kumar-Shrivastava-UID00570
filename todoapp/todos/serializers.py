from rest_framework import serializers

from todos import models as todo_models
from users import models as user_models


class TodoSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(
        source='date_created', format="%I:%M %p, %d %b, %Y"
    )

    def get_status(self, obj):
        return "Done" if obj.done else "To Do"

    def get_creator(self, obj):
        return {
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'email': obj.user.email
        }

    class Meta:
        model = todo_models.Todo
        fields = ['id', 'name', 'status', 'created_at', 'creator']


class TodosWithinDateRangeSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email')
    created_at = serializers.DateTimeField(
        source='date_created', format="%I:%M %p, %d %b, %Y"
    )

    def get_status(self, obj):
        return "Done" if obj.done else "To Do"

    def get_creator(self, obj):
        return obj.user.first_name + " " + obj.user.last_name

    class Meta:
        model = todo_models.Todo
        fields = ['id', 'name', 'creator', 'email', 'created_at', 'status']


class UserTodoStatsSerializer(serializers.ModelSerializer):
    completed_count = serializers.IntegerField()
    pending_count = serializers.IntegerField()

    class Meta:
        model = user_models.CustomUser
        fields = [
            'id', 'first_name', 'last_name', 'email', 'completed_count', 'pending_count'
        ]


class UserTodoReportSerializer(serializers.ModelSerializer):
    completed_count = serializers.IntegerField()
    pending_count = serializers.IntegerField()

    class Meta:
        model = user_models.CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'completed_count', 'pending_count'
        ]


class PendingTodosSerializer(serializers.ModelSerializer):
    pending_count = serializers.IntegerField()

    class Meta:
        model = user_models.CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'pending_count']


class TodoAPICreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    done = serializers.BooleanField(read_only=True)
    date_created = serializers.DateTimeField(read_only=True)

    todo = serializers.CharField(source='name', write_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(),
                                                 source='user', write_only=True)

    class Meta:
        model = Todo
        fields = ['user_id', 'todo', 'name', 'done', 'date_created']


class TodoAPIResponseSerializer(serializers.ModelSerializer):
    todo_id = serializers.IntegerField(source='id')
    todo = serializers.CharField(source='name')

    class Meta:
        model = Todo
        fields = ['todo_id', 'todo', 'done']
