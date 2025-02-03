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
