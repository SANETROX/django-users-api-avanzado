from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

def sample_user(email='camilo@gmail.com',password='1234passcamilo'):
    return get_user_model().objects.create_user(
        email,
        password
    )

class MoldelTest(TestCase):

    def test_create_user_with_email(self):
        """ Probar creando un  nuevo user con un email correctamente"""

        email = 'test@gmail.com'
        password = 'testpassword123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_normalized(self):
        """"testea email para nuevo usuario normalizado"""
        email = "test2@GMAIL.COM"
        password = "test2456"

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email.lower())
    
    def test_new_user_invalid_email(self):
        """TEst para nuevo user email invalido"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
            email=None
        )
    
    def test_create_new_superuser(self):
        """"Test para un nuevo superuser"""
        email = 'testsuperuser@gmail.com'
        password = 'testpassword123'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    
    def test_tag_str(self):
        """Probasr representacion de cadena de texto del tag"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Meat'
        )

        self. assertEqual(str(tag), tag.name)