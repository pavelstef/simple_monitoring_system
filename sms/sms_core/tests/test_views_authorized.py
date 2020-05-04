""" Tests for sms_core views for authorized users. """

from django.test import TestCase
from django.urls import reverse

from sms_core.models import SmsUser, Device
from sms_core.forms import UserCreationForm, UserChangeForm, DeviceForm


class LoginLogoutViewTests(TestCase):
    """ A class which prepares test data for tests of Login and Logout views """

    @classmethod
    def setUpTestData(cls) -> None:
        admin = SmsUser.objects.create_superuser(
            name='test_admin', password='test_admin'
        )
        admin.save()
        user = SmsUser.objects.create_user(
            name='test_user', password='test_user')
        user.save()


class SmsLogInViewTests(LoginLogoutViewTests):
    """ Tests for the Login view """

    def test_admin_login(self) -> None:
        self.client.login(username='test_admin', password='test_admin')
        response = self.client.get(reverse('url_login'))
        self.assertEqual(str(response.context['user']), 'test_admin')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sms_core/sms_log_in.html')

    def test_user_login(self) -> None:
        self.client.login(username='test_user', password='test_user')
        response = self.client.get(reverse('url_login'))
        self.assertEqual(str(response.context['user']), 'test_user')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sms_core/sms_log_in.html')


class SmsLogOutViewTests(LoginLogoutViewTests):
    """ Tests for the Logout view """

    def test_admin_logout(self) -> None:
        response = self.client.get(reverse('url_logout'))
        self.assertEqual(response.context, None)
        self.assertRedirects(
            response,
            expected_url=reverse('url_login'),
            status_code=302,
            target_status_code=200
        )

    def test_user_logout(self) -> None:
        response = self.client.get(reverse('url_logout'))
        self.assertEqual(response.context, None)
        self.assertRedirects(
            response,
            expected_url=reverse('url_login'),
            status_code=302,
            target_status_code=200
        )


class OperationalViewTests(TestCase):
    """ A class which prepares test data for tests of operational views """

    @classmethod
    def setUpTestData(cls) -> None:
        admin1 = SmsUser.objects.create_superuser(
            name='test_admin1', password='test_admin1'
        )
        admin1.save()
        admin2 = SmsUser.objects.create_superuser(
            name='test_admin2', password='test_admin2'
        )
        admin2.save()
        user = SmsUser.objects.create_user(
            name='test_user', password='test_user')
        user.save()
        Device.objects.create(
            name='device1',
            ip_fqdn='1.1.1.1',
            description='Device 1 description',
            updated_by=admin1
        )
        Device.objects.create(
            name='device2',
            ip_fqdn='2.2.2.2',
            updated_by=admin2
        )


class SmsOverviewViewTests(OperationalViewTests):
    """ Tests for the SmsOverviewView """

    def tearDown(self) -> None:
        self.client.logout()

    def test_overview_admin(self) -> None:
        self.client.login(username='test_admin1', password='test_admin1')
        response = self.client.get(reverse('url_devices_overview'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sms_core/sms_overview.html')

        # Checking that the user has administrative privileges
        self.assertTrue(response.context['user'].is_staff)

        # Checking quantity observed devices.
        self.assertEqual(len(response.context['devices']), 2)

        # Checking that buttons that should be accessible only to the
        # administrator.  The buttons should be accessible.
        self.assertContains(response, 'href="/sms/administration/')
        self.assertContains(response, 'href="/sms/device/add/')
        self.assertContains(response, 'href="/sms/device/edit/')

    def test_overview_user(self) -> None:
        self.client.login(username='test_user', password='test_user')
        response = self.client.get(reverse('url_devices_overview'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sms_core/sms_overview.html')

        # Checking that the user has no administrative privileges
        self.assertFalse(response.context['user'].is_staff)

        # Checking quantity observed devices.
        self.assertEqual(len(response.context['devices']), 2)

        # Checking that buttons that should be accessible only to the
        # administrator.  The buttons should be NOT accessible.
        self.assertNotContains(response, 'href="/sms/administration/')
        self.assertNotContains(response, 'href="/sms/device/add/')
        self.assertNotContains(response, 'href="/sms/device/edit/')

    def test_search(self) -> None:
        self.client.login(username='test_admin1', password='test_admin1')
        response = self.client.get(
            f'{reverse("url_devices_overview")}?search=device2'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sms_core/sms_overview.html')

        # Checking quantity observed devices.
        self.assertEqual(len(response.context['devices']), 1)
        # Checking the device name.
        self.assertEqual(str(response.context['devices'][0]), 'device2')


class SmsAdministrationViewTests(OperationalViewTests):
    """ Tests for the SmsOverviewView """

    def setUp(self) -> None:
        self.client.login(username='test_admin1', password='test_admin1')

    def test_administration(self) -> None:
        response = self.client.get(reverse('url_administration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sms_core/sms_administration.html')

        # Checking that the user has administrative privileges
        self.assertTrue(response.context['user'].is_staff)

        # Checking quantity users.
        self.assertEqual(len(response.context['smsusers']), 3)

        # Checking that buttons that should be accessible only to the
        # administrator.  The buttons should be accessible.
        self.assertContains(response, 'href="/sms/user/create/"')
        self.assertContains(response, 'href="/sms/user/delete/')

    def test_search(self) -> None:
        response = self.client.get(
            f'{reverse("url_administration")}?search=user'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sms_core/sms_administration.html')

        # Checking quantity users.
        self.assertEqual(len(response.context['smsusers']), 1)
        # Checking the device name.
        self.assertEqual(str(response.context['smsusers'][0]), 'test_user')


class SmsDeviceDetailsViewTests(OperationalViewTests):
    """ Tests for the SmsDeviceDetailsView """

    def setUp(self) -> None:
        self.client.login(username='test_admin1', password='test_admin1')

    def test_device_detail(self) -> None:
        device = Device.objects.get(name='device1')
        response = self.client.get(
            reverse('url_device_detail', kwargs={'slug': device.name})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sms_core/sms_device_detail.html')
        self.assertEqual(response.context['device'], device)


class SmsDeviceAddViewTests(OperationalViewTests):
    """ Tests for the SmsDeviceAddView """

    def setUp(self) -> None:
        self.client.login(username='test_admin1', password='test_admin1')

    def test_device_add_get(self) -> None:
        response = self.client.get(reverse('url_device_add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sms_core/sms_device_add.html')
        self.assertIsInstance(response.context['form'], DeviceForm)

    def test_device_add_post_valid(self) -> None:
        data = {
            'name': 'device3',
            'ip_fqdn': '3.3.3.3',
            'description': 'Device 3 description',
            'check_interval': 10
        }
        response = self.client.post(reverse('url_device_add'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['success'])
        new_device = Device.objects.get(name=data['name'])
        self.assertEqual(new_device.name, data['name'])
        self.assertEqual(new_device.ip_fqdn, data['ip_fqdn'])
        self.assertEqual(new_device.description, data['description'])
        self.assertEqual(new_device.check_interval, data['check_interval'])
        self.assertEqual(str(new_device.updated_by), 'test_admin1')

    def test_device_add_post_invalid(self) -> None:
        data = {
            'name': 'device 4',  # invalid name
            'ip_fqdn': '3.3.3.3',
            'description': 'Device 3 description',
            'check_interval': 10
        }
        response = self.client.post(reverse('url_device_add'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['success'])
        with self.assertRaises(Device.DoesNotExist):
            Device.objects.get(name=data['name'])


class SmsDeviceEditViewTests(OperationalViewTests):
    """ Tests for the SmsDeviceEditView """

    def setUp(self) -> None:
        self.client.login(username='test_admin1', password='test_admin1')
        self.device = Device.objects.get(name='device1')

    def test_device_edit_get(self) -> None:
        response = self.client.get(
            reverse('url_device_edit', kwargs={'slug': self.device.name})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sms_core/sms_device_edit.html')
        self.assertIsInstance(response.context['form'], DeviceForm)
        self.assertEqual(response.context['obj'], self.device)

    def test_device_edit_post_valid(self) -> None:
        data = {
            'name': 'device1',
            'ip_fqdn': '11.11.11.11',
            'description': 'Device 1 new description',
            'check_interval': 30
        }
        response = self.client.post(
            reverse('url_device_edit', kwargs={'slug': self.device.name}),
            data=data
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['success'])
        updated_device = Device.objects.get(name=data['name'])
        self.assertEqual(updated_device.name, data['name'])
        self.assertEqual(updated_device.ip_fqdn, data['ip_fqdn'])
        self.assertEqual(updated_device.description, data['description'])
        self.assertEqual(updated_device.check_interval, data['check_interval'])
        self.assertEqual(str(updated_device.updated_by), 'test_admin1')

    def test_device_edit_post_invalid(self) -> None:
        data = {
            'name': 'device 1',  # invalid name
            'ip_fqdn': '11.11.11.11',
            'description': 'Device 1 new description',
            'check_interval': 30
        }
        response = self.client.post(
            reverse('url_device_edit', kwargs={'slug': self.device.name}),
            data=data
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['success'])
        with self.assertRaises(Device.DoesNotExist):
            Device.objects.get(name=data['name'])


class SmsDeviceDeleteViewTests(OperationalViewTests):
    """ Tests for the SmsDeviceDeleteView """

    def setUp(self) -> None:
        self.client.login(username='test_admin1', password='test_admin1')
        self.device = Device.objects.get(name='device1')

    def test_device_delete_get(self) -> None:
        response = self.client.get(
            reverse('url_device_dell', kwargs={'slug': self.device.name})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sms_core/sms_confirmation.html')
        self.assertEqual(
            response.context['redirect_url'],
            'url_devices_overview'
        )
        self.assertEqual(response.context['obj'], self.device)

    def test_device_delete_post(self) -> None:
        response = self.client.post(
            reverse('url_device_dell', kwargs={'slug': self.device.name})
        )
        self.assertRedirects(
            response=response,
            expected_url=reverse('url_devices_overview'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )
        with self.assertRaises(Device.DoesNotExist):
            Device.objects.get(name=self.device.name)


class SmsUserCreateViewTests(OperationalViewTests):
    """ Tests for the SmsUserCreateView """

    def setUp(self) -> None:
        self.client.login(username='test_admin1', password='test_admin1')

    def test_user_create_get(self) -> None:
        response = self.client.get(reverse('url_user_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sms_core/sms_user_create.html')
        self.assertIsInstance(response.context['form'], UserCreationForm)

    def test_user_create_post_user(self) -> None:
        data = {
            'name': 'test_user3',
            'password1': 'test_user3',
            'password2': 'test_user3',
            'is_staff': False
        }
        response = self.client.post(reverse('url_user_create'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['success'])
        new_user = SmsUser.objects.get(name=data['name'])
        self.assertEqual(new_user.name, data['name'])
        self.assertEqual(new_user.is_staff, data['is_staff'])

    def test_user_create_post_admin(self) -> None:
        data = {
            'name': 'test_admin3',
            'password1': 'test_admin3',
            'password2': 'test_admin3',
            'is_staff': True
        }
        response = self.client.post(reverse('url_user_create'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['success'])
        new_user = SmsUser.objects.get(name=data['name'])
        self.assertEqual(new_user.name, data['name'])
        self.assertEqual(new_user.is_staff, data['is_staff'])

    def test_user_create_post_invalid(self) -> None:
        data = {
            'name': 'test admin3',  # invalid name
            'password1': 'test_admin3',
            'password2': 'test_admin3',
            'is_staff': True
        }
        response = self.client.post(reverse('url_user_create'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['success'])
        with self.assertRaises(SmsUser.DoesNotExist):
            SmsUser.objects.get(name=data['name'])


class SmsUserEditViewTests(OperationalViewTests):
    """ Tests for the SmsUserEditView """

    def setUp(self) -> None:
        self.client.login(username='test_admin2', password='test_admin2')
        self.user = SmsUser.objects.get(name='test_admin2')

    def test_user_edit_get(self) -> None:
        response = self.client.get(
            reverse('url_user_edit', kwargs={'slug': self.user.name})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sms_core/sms_user_edit.html')
        self.assertIsInstance(response.context['form'], UserChangeForm)
        self.assertEqual(response.context['obj'], self.user)

    def test_user_edit_post_valid(self) -> None:
        data = {
            'name': self.user.name,
            'password1': 'test_admin2_new',
            'password2': 'test_admin2_new'
        }
        response = self.client.post(
            reverse('url_user_edit', kwargs={'slug': self.user.name}),
            data=data
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['success'])

    def test_user_edit_post_invalid(self) -> None:
        data = {
            'name': self.user.name,
            'password1': 'test_admin2_new',
            'password2': 'test_admin2_new1'  # invalid password2
        }
        response = self.client.post(
            reverse('url_user_edit', kwargs={'slug': self.user.name}),
            data=data
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['success'])


class SmsUserDeleteViewTests(OperationalViewTests):
    """ Tests for the SmsUserDeleteView """

    def setUp(self) -> None:
        self.client.login(username='test_admin1', password='test_admin1')
        self.user = SmsUser.objects.get(name='test_admin2')

    def test_user_delete_get(self) -> None:
        response = self.client.get(
            reverse('url_user_dell', kwargs={'slug': self.user.name})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sms_core/sms_confirmation.html')
        self.assertEqual(
            response.context['redirect_url'],
            'url_administration'
        )
        self.assertEqual(response.context['obj'], self.user)

    def test_user_delete_post(self) -> None:
        response = self.client.post(
            reverse('url_user_dell', kwargs={'slug': self.user.name})
        )
        self.assertRedirects(
            response=response,
            expected_url=reverse('url_administration'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )
        with self.assertRaises(SmsUser.DoesNotExist):
            SmsUser.objects.get(name=self.user.name)

    def test_user_delete_post_last_admin(self) -> None:
        """ The view should not delete user if user is the last active admin. """

        # Deleting another admin user
        self.user.set_deleted()

        response = self.client.post(
            reverse('url_user_dell', kwargs={'slug': 'test_admin1'})
        )
        self.assertRedirects(
            response=response,
            expected_url=reverse('url_administration'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )
        # Check that the user still exists and is the admin.
        self.assertTrue(SmsUser.objects.get(name='test_admin1').is_staff)
