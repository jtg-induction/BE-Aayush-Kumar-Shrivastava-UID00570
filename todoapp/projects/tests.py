from django.test import TestCase
from django.urls import reverse

from model_bakery import baker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from projects import models as project_models
from users import models as user_models


class ProjectMemberApiViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.project = baker.make(
            project_models.Project, name="Project1", max_members=3
        )
        self.users = baker.make(user_models.CustomUser, _quantity=5)
        self.token = Token.objects.create(user=self.users[0])
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.add_url = reverse(
            'project-action', kwargs={'pk': self.project.id, 'action': 'add'}
        )
        self.remove_url = reverse(
            'project-action', kwargs={'pk': self.project.id, 'action': 'remove'}
        )

    def test_add_member_to_project(self):
        response = self.client.patch(
            self.add_url, 
            {'user_ids': [self.users[1].id, self.users[2].id]}, 
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.users[1], self.project.members.all())
        self.assertIn(self.users[2], self.project.members.all())
        self.assertEqual(
            response.data['logs'][self.users[1].id], 'Member added Successfully'
        )
        self.assertEqual(
            response.data['logs'][self.users[2].id], 'Member added Successfully'
        )

    def test_maxmember_add_member_to_project(self):
        self.project.members.add(self.users[1], self.users[2], self.users[3])

        response = self.client.patch(
            self.add_url, {'user_ids': [self.users[4].id]}, format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data['logs'][self.users[4].id], "Max Member Limit Reached"
        )

    def test_remove_member_to_project(self):
        self.project.members.add(self.users[1])
        response = self.client.patch(
            self.remove_url, 
            {'user_ids': [self.users[1].id, self.users[2].id]}, 
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.users[1], self.project.members.all())
        self.assertEqual(
            response.data['logs'][self.users[1].id], 'User removed Succesfully'
        )
        self.assertEqual(
            response.data['logs'][self.users[2].id], 'User is not a Member'
        )
