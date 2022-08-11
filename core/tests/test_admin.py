from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'camilo12@gmail.com',
            password = '12234@cami'
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email = 'camilouser@gmail.com',
            password = '1224@camilo',
            name = 'testusername'
        )
    
    def test_user_listed(self):
        """Testea si los users han sido enlistados en la pagina"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        print("RESPONSE", res)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
    
    def test_user_change_page(self):
        """ Purbea que la pagina editada para el User funcione"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code,200)

    def test_create_user_page(self):
        """Testear que la pagina de crear users funcione"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code,200)





