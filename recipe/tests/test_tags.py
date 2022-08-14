from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')

class PublicTagsApiTests(TestCase):
    """Probar los tags disponibles publicamente"""

    def setUp(self):
        self.client = APIClient()
    
    def test_login_required(self):
        """Probar que login sea requerido para obtener los tags"""

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code,status.HTTP_403_FORBIDDEN)


class PrivateTagsApiTests(TestCase):
    """Probar los tags disponibles privados"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'pass12345@'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
    
    def test_retrieve_tags(self):
        """"Probar obtener los tags"""
        Tag.objects.create(user=self.user, name="drinks")
        Tag.objects.create(user=self.user, name="banana")

        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def tests_tags_limited_to_user(self):
        """"Probar que los tags retornado son del user"""

        user2 = get_user_model().objects.create_user(
            "otrouser@gmail.com",
            "otropass123"
        )
        Tag.objects.create(user=user2, name="Fast Food")
        tag = Tag.objects.create(user=self.user, name="Fit Food")
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        print(res.data)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'],tag.name)