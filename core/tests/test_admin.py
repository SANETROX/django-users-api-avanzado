from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setup(self):
        """"Funcion que se corre antes de hacer todo los test"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admintest@gmail.com',
            password='admintest123'
        )
        self.client.force_login(self.admin_user) #)bliga a que siempre haga login
        self.user = get_user_model.objects.create_user(
            email='user@gmail.com',
            password='pass1234',
            name='Test User Nombre Completo'
        )

    def test_users_listed(self):
        """"Testea que los users han sido enlistados en la pagina del user"""
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.email.name)