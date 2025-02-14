from django.urls import reverse

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from projects import models as project_models 
from users import models as user_models


class MembersViewSetSerializerTest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        
        self.project = project_models.Project.objects.create(name='TEST PROJECT', max_members=2)
        
        self.user1 = user_models.CustomUser.objects.create_user(
            email="test@testuser1.com",
            password="123123",
            first_name="John", 
            last_name="Doe"
        )
        self.user2 = user_models.CustomUser.objects.create_user(
            email="test@testuser2.com",
            password="123123",
            first_name="John", 
            last_name="Doe"
        )
        self.user3 = user_models.CustomUser.objects.create_user(
            email="test@testuser3.com",
            password="123123",
            first_name="John", 
            last_name="Doe"
        )
        
        self.token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.add_url = reverse('project-action', kwargs={'pk': self.project.id, 'action': 'add'})
        self.remove_url = reverse('project-action', kwargs={'pk': self.project.id, 'action': 'remove'})
        
    def test_add_member_to_project(self):
        response = self.client.patch(self.add_url, {'user_ids': [self.user1.id, self.user2.id]}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user1, self.project.members.all())
        self.assertEqual(response.data['logs'][self.user1.id], 'Member added Successfully')
        
    def test_add_and_remove_member_to_project(self):
        response = self.client.patch(self.add_url, {'user_ids': [self.user1.id, self.user2.id]}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user1, self.project.members.all())
        self.assertEqual(response.data['logs'][self.user1.id], 'Member added Successfully')
        
        response = self.client.patch(self.remove_url, {'user_ids': [self.user1.id]}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.user1, self.project.members.all())
        self.assertEqual(response.data['logs'][self.user1.id], 'User removed Succesfully')