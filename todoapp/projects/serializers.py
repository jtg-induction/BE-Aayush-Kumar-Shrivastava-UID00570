from rest_framework import serializers
from .models import Project
from users import serializers as user_serializers

class ProjectSerializer(serializers.ModelSerializer):
    existing_member_count = serializers.IntegerField()
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.STATUS_CHOICES[obj.status][1]

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'status', 'existing_member_count', 'max_members'
        ]


class ProjectReportSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='name')
    report = serializers.SerializerMethodField(source='reports')

    def get_report(self, obj):
        reports =  user_serializers.UserTodoStatsSerializer(obj.reports, many=True, context={"exclude_id": True}).data
        
        for report in reports:
            report.pop('id', None)
            
        return reports 
    
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
