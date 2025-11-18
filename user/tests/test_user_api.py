from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import User

USER_CREATE_URL = reverse('user-create')

class UserApiTests(APITestCase):
    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'apiuser@example.com',
            'name': 'API User',
            'password': 'ApiPass123'
        }
        res = self.client.post(USER_CREATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertEqual(user.name, payload['name'])
        self.assertNotIn('password', res.data)

    def test_create_user_with_existing_email(self):
        """Test creating user with email that already exists fails"""
        User.objects.create_user(email='dup@example.com', name='Dup', password='dup123')
        payload = {
            'email': 'dup@example.com',
            'name': 'Dup 2',
            'password': 'dup456'
        }
        res = self.client.post(USER_CREATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_missing_data(self):
        """Test creating user with missing fields fails"""
        payload = {'email': '', 'name': '', 'password': ''}
        res = self.client.post(USER_CREATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', res.data)
        self.assertIn('name', res.data)
        self.assertIn('password', res.data)

    def test_create_user_invalid_email(self):
        """Test creating user with invalid email fails"""
        payload = {
            'email': 'bademail',
            'name': 'Bad Email',
            'password': 'abc12345'
        }
        res = self.client.post(USER_CREATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', res.data)

    def test_create_user_short_password(self):
        """Test password less than 8 chars fails (assuming validator exists)"""
        payload = {
            'email': 'shortpass@example.com',
            'name': 'Short Pass',
            'password': 'shrt'
        }
        res = self.client.post(USER_CREATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', res.data)
