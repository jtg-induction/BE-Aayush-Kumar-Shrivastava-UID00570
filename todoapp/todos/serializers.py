from rest_framework import serializers

from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(
        source='date_created', format="%I:%M %p, %d %b, %Y")

    def get_status(self, obj):
        return "Done" if obj.done else "To Do"

    def get_creator(self, obj):
        return {
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'email': obj.user.email
        }

    class Meta:
        model = Todo
        fields = ['id', 'name', 'status', 'created_at', 'creator']


class TodosWithinDateRangeSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email')
    created_at = serializers.DateTimeField(
        source='date_created', format="%I:%M %p, %d %b, %Y")

    def get_status(self, obj):
        return "Done" if obj.done else "To Do"

    def get_creator(self, obj):
        return obj.user.first_name + " " + obj.user.last_name

    class Meta:
        model = Todo
        fields = ['id', 'name', 'creator', 'email', 'created_at', 'status']


class TodoAPICreateSerializer(serializers.ModelSerializer):
    todo = serializers.CharField(source='name', write_only=True)

    class Meta:
        model = Todo
        fields = ['todo', 'name', 'done', 'date_created']
        read_only_fields = ['name', 'done', 'date_created']

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        return super().create(validated_data)


class TodoAPIResponseSerializer(serializers.ModelSerializer):
    todo_id = serializers.IntegerField(source='id')
    todo = serializers.CharField(source='name')

    class Meta:
        model = Todo
        fields = ['todo_id', 'todo', 'done']
