from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    existing_member_count = serializers.IntegerField()
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.STATUS_CHOICES[obj.status][1]

    class Meta:
        model = Project
        fields = ['id', 'name', 'status',
                  'existing_member_count', 'max_members']


class ProjectReportSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='name')
    report = serializers.SerializerMethodField()

    def get_report(self, obj):
        user_reports = []
        for user in obj.reports:
            user_report = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'pending_count': user.pending_count,
                'completed_count': user.completed_count
            }
            user_reports.append(user_report)
        return user_reports

    class Meta:
        model = Project
        fields = ['project_title', 'report']


class ProjectWithMemberNameSerializer(serializers.ModelSerializer):
    done = serializers.SerializerMethodField()
    project_name = serializers.CharField(source='name')

    def get_done(self, obj):
        return True if obj.status == 2 else False

    class Meta:
        model = Project
        fields = ['project_name', 'done', 'max_members']
