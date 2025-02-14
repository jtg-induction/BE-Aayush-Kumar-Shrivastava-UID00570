from django.contrib.postgres.aggregates import ArrayAgg

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


class MembersViewSetSerializer(serializers.ModelSerializer):
    user_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=user_models.CustomUser.objects.all(), write_only=True)

    def update(self, instance, validated_data):
        request = self.context.get('request', None)

        member_ids = set(user.id for user in validated_data['user_ids'])
        project_member_list = instance.members.values_list('id', flat=True)

        logs = {}

        if (request and 'add' in request.path):
            user_project_data = list(user_models.CustomUser.objects.filter(id__in=member_ids).annotate(
                projectwork=ArrayAgg('projectmember__project__id')
            ))

            add_user_list = []

            for user in user_project_data:
                if user.id in project_member_list:
                    logs[user.id] = 'User is already a Member'
                elif len(user.projectwork) >= 2:
                    logs[user.id] = 'Cannot add as User is a member in two projects'
                elif len(project_member_list) >= instance.max_members:
                    logs[user.id] = 'Max Member Limit Reached'
                    break
                else:
                    add_user_list.append(user)
                    logs[user.id] = 'Member added Successfully'

            project_members = [
                project_models.ProjectMember(project=instance, member=user) for user in add_user_list
            ]
            project_models.ProjectMember.objects.bulk_create(project_members)

        else:
            remove_user_list = []

            for user_id in member_ids:
                if user_id in project_member_list:
                    remove_user_list.append(user_id)
                    logs[user_id] = 'User removed Succesfully'
                else:
                    logs[user_id] = 'User is not a Member'

            project_models.ProjectMember.objects.filter(
                project_id=instance.id, member_id__in=remove_user_list).delete()

        self.context['logs'] = logs
        return instance

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data['logs'] = self.context.get('logs', {})

        return data

    class Meta:
        model = project_models.Project
        fields = ['user_ids']


class DefaultProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = project_models.Project
        fields = '__all__'
