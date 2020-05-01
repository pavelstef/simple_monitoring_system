""" Tests for sms_core views and general redirection views. """

from django.test import SimpleTestCase
from django.urls import reverse


class URLTestsCommon(SimpleTestCase):
    """ Tests access to common pages """

    def test_homepage_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 301)

    def test_login_redirect(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 301)

    def test_login_page(self):
        response = self.client.get(reverse('url_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sms_core/sms_log_in.html')

    def test_logout_page_redirect(self):
        response = self.client.get(reverse('url_logout'))
        self.assertEqual(response.status_code, 302)


class URLTestsUnauthorized(SimpleTestCase):
    """
    Tests access unauthorized user to protected pages.
    All of the pages should redirect unauthorized user to the login page.
    """

    def test_devices_overview_page(self):
        response = self.client.get(reverse('url_devices_overview'))
        self.assertEqual(response.status_code, 302)

    def test_administration_page(self):
        response = self.client.get(reverse('url_administration'))
        self.assertEqual(response.status_code, 302)

    def test_user_create_page(self):
        response = self.client.get(reverse('url_user_create'))
        self.assertEqual(response.status_code, 302)

    def test_user_edit_page(self):
        response = self.client.get(reverse('url_user_edit', kwargs={'slug': 'test'}))
        self.assertEqual(response.status_code, 302)

    def test_user_dell_page(self):
        response = self.client.get(reverse('url_user_dell', kwargs={'slug': 'test'}))
        self.assertEqual(response.status_code, 302)

    def test_device_add_page(self):
        response = self.client.get(reverse('url_device_add'))
        self.assertEqual(response.status_code, 302)

    def test_device_edit_page(self):
        response = self.client.get(reverse('url_device_edit', kwargs={'slug': 'test'}))
        self.assertEqual(response.status_code, 302)

    def test_device_detail_page(self):
        response = self.client.get(reverse('url_device_detail', kwargs={'slug': 'test'}))
        self.assertEqual(response.status_code, 302)

    def test_device_dell_page(self):
        response = self.client.get(reverse('url_device_dell', kwargs={'slug': 'test'}))
        self.assertEqual(response.status_code, 302)
