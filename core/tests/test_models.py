from django.test import TestCase
from core.models import User

class UserModelTests(TestCase):
    
    def test_create_user_with_email_successful(self):
        """Test creating a new user with email is successful and email is normalized"""
        email = 'test@example.COM'
        name = 'Test User'
        password = 'Testpass123'
        user = User.objects.create_user(email=email, name=name, password=password)

        # Check email normalization
        self.assertEqual(user.email, email.lower())
        # Check password is set correctly
        self.assertTrue(user.check_password(password))
        # Check default flags
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser works correctly"""
        email = 'admin@example.com'
        name = 'Admin User'
        password = 'AdminPass123'
        admin_user = User.objects.create_superuser(email=email, name=name, password=password)

        # Superuser flags
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_active)

    def test_user_str_method(self):
        """Test the __str__ method returns email"""
        user = User.objects.create_user(email='user@example.com', name='User Name', password='Testpass123')
        self.assertEqual(str(user), 'user@example.com')
