""" Tests for sms_core views and general redirection views. """

from django.test import SimpleTestCase
from django.urls import reverse


class URLCommonTests(SimpleTestCase):
    """ Tests access to common pages """

    def test_homepage_redirect(self) -> None:
        response = self.client.get('/')
        self.assertRedirects(
            response=response,
            expected_url='/sms/overview/',
            status_code=301,
            target_status_code=302,
            fetch_redirect_response=True
        )

    def test_login_redirect(self) -> None:
        response = self.client.get('/accounts/login/')
        self.assertRedirects(
            response=response,
            expected_url='/sms/login/',
            status_code=301,
            target_status_code=200,
            fetch_redirect_response=True
        )

    def test_login_page(self) -> None:
        response = self.client.get(reverse('sms_core:url_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sms_core/sms_log_in.html')

    def test_logout_page_redirect(self) -> None:
        response = self.client.get(reverse('sms_core:url_logout'))
        self.assertRedirects(
            response=response,
            expected_url='/sms/login/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )


class ViewsUnauthorizedTests(SimpleTestCase):
    """
    Tests access unauthorized user to protected pages.
    All of the pages should redirect unauthorized user to the login page.
    """

    def test_devices_overview_page(self) -> None:
        response = self.client.get(reverse('sms_core:url_devices_overview'))
        self.assertRedirects(
            response=response,
            expected_url='/accounts/login/?next=/sms/overview/',
            status_code=302,
            target_status_code=301,
            fetch_redirect_response=True
        )

    def test_administration_page(self) -> None:
        response = self.client.get(reverse('sms_core:url_administration'))
        self.assertRedirects(
            response=response,
            expected_url='/accounts/login/?next=/sms/administration/',
            status_code=302,
            target_status_code=301,
            fetch_redirect_response=True
        )

    def test_user_create_page(self) -> None:
        response = self.client.get(reverse('sms_core:url_user_create'))
        self.assertRedirects(
            response=response,
            expected_url='/accounts/login/?next=/sms/user/create/',
            status_code=302,
            target_status_code=301,
            fetch_redirect_response=True
        )

    def test_user_edit_page(self) -> None:
        response = self.client.get(
            reverse('sms_core:url_user_edit', kwargs={'slug': 'test'})
        )
        self.assertRedirects(
            response=response,
            expected_url='/accounts/login/?next=/sms/user/edit/test/',
            status_code=302,
            target_status_code=301,
            fetch_redirect_response=True
        )

    def test_user_dell_page(self) -> None:
        response = self.client.get(
            reverse('sms_core:url_user_dell', kwargs={'slug': 'test'})
        )
        self.assertRedirects(
            response=response,
            expected_url='/accounts/login/?next=/sms/user/delete/test/',
            status_code=302,
            target_status_code=301,
            fetch_redirect_response=True
        )

    def test_device_add_page(self) -> None:
        response = self.client.get(reverse('sms_core:url_device_add'))
        self.assertRedirects(
            response=response,
            expected_url='/accounts/login/?next=/sms/device/add/',
            status_code=302,
            target_status_code=301,
            fetch_redirect_response=True
        )

    def test_device_edit_page(self) -> None:
        response = self.client.get(
            reverse('sms_core:url_device_edit', kwargs={'slug': 'test'})
        )
        self.assertRedirects(
            response=response,
            expected_url='/accounts/login/?next=/sms/device/edit/test/',
            status_code=302,
            target_status_code=301,
            fetch_redirect_response=True
        )

    def test_device_detail_page(self) -> None:
        response = self.client.get(
            reverse('sms_core:url_device_detail', kwargs={'slug': 'test'})
        )
        self.assertRedirects(
            response=response,
            expected_url='/accounts/login/?next=/sms/device/detail/test/',
            status_code=302,
            target_status_code=301,
            fetch_redirect_response=True
        )

    def test_device_dell_page(self) -> None:
        response = self.client.get(
            reverse('sms_core:url_device_dell', kwargs={'slug': 'test'})
        )
        self.assertRedirects(
            response=response,
            expected_url='/accounts/login/?next=/sms/device/delete/test/',
            status_code=302,
            target_status_code=301,
            fetch_redirect_response=True
        )
