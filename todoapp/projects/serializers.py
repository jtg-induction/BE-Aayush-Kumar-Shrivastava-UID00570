from rest_framework import serializers

from projects import models as project_models
from todos import serializers as todo_serializers 
from users import models as user_models


class ProjectSerializer(serializers.ModelSerializer):
    existing_member_count = serializers.IntegerField()
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.STATUS_CHOICES[obj.status][1]

    class Meta:
        model = project_models.Project
        fields = [
            'id', 'name', 'status', 'existing_member_count', 'max_members'
        ]


class ProjectReportSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='name')
    report = todo_serializers.UserTodoReportSerializer(source='reports', many=True)
    
    class Meta:
        model = project_models.Project
        fields = ['project_title', 'report']


class ProjectWithMemberNameSerializer(serializers.ModelSerializer):
    done = serializers.SerializerMethodField()
    project_name = serializers.CharField(source='name')

    def get_done(self, obj):
        return True if obj.status == 2 else False

    class Meta:
        model = project_models.Project
        fields = ['project_name', 'done', 'max_members']


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
