from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(
        **params
    )


class PublicUserApiTests(TestCase):
    """el publico no esta autenticado"""
    def setUp(self):
        self.client = APIClient()
    
    def test_create_valid_user(self):
        """Testy para crear un user valido"""
        payload = {
            "email": "camilo@gmail.com",
            "password": "pass1234@",
            "name": "sanetrox"
        }

        res = self.client.post(CREATE_USER_URL, payload)
        print("response create_valid_user_api", res)

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password",res.data)
    
    def test_user_exists(self):
        """Test para probar que un user ya existe"""
        payload = {
            "email": "camilo@gmail.com",
            "password": "pass1234@",
            "name": "sanetrox"
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_short(self):
        """"Test para validar una password corta"""
        payload = {
            "email": "camilo@gmail.com",
            "password": "pa112",
            "name": "sanetrox"
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        user_exists = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Probar que el token es creado por el user"""
        payload = {
            "email": "camilo@gmail.com",
            "password": "pa112",
            "name": "sanetrox"
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_create_token_invalid_credentials(self):
        """Probar que el token no es creado con credenciales invalidas"""

        create_user(email='sanetrox@gmail.com', password='password1233')
        payload = {'email':"sanetrox@gmail.com", 'password':'1234'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_no_user(self):
        """"Prueba que no se cree un token cuando un user no existe"""

        payload = {
            "email": "camilo12@gmail.com",
            "password": "pa112sadas",
            "name": "sanetrox1"
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Probar que no se cree token cuando faltan campos"""
        payload = {
            "email": "",
            "password": ""
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)