""" Tests for sms_core models. """

from django.test import TestCase
from django.utils import timezone, dateformat

from sms_core.models import SmsUser, Device


class SmsUserModelTests(TestCase):
    """ Test for custom user model SmsUser """

    model = SmsUser

    @classmethod
    def setUpTestData(cls) -> None:
        SmsUser.objects.create_superuser(
            name='test_admin', password='test_admin'
        )
        SmsUser.objects.create_user(name='test_user', password='test_user')

    def test_get_absolute_url(self) -> None:
        admin = self.model.objects.get(name='test_admin')
        user = self.model.objects.get(name='test_user')
        self.assertEqual(admin.get_absolute_url(), '/sms/user/edit/test_admin/')
        self.assertEqual(user.get_absolute_url(), '/sms/user/edit/test_user/')

    def test_get_delete_url(self) -> None:
        admin = self.model.objects.get(name='test_admin')
        user = self.model.objects.get(name='test_user')
        self.assertEqual(admin.get_delete_url(), '/sms/user/delete/test_admin/')
        self.assertEqual(user.get_delete_url(), '/sms/user/delete/test_user/')

    def test_set_deleted(self) -> None:
        admin = self.model.objects.get(name='test_admin')
        user = self.model.objects.get(name='test_user')
        admin.set_deleted()
        user.set_deleted()
        self.assertFalse(admin.is_active)
        self.assertFalse(user.is_active)
        # The name must be changed on <name>_deleted_at_<date and time>
        self.assertEqual(
            admin.name,
            f'test_admin_deleted_at_{dateformat.format(timezone.now(), "Y-m-d_H:i")}'
        )
        self.assertEqual(
            user.name,
            f'test_user_deleted_at_{dateformat.format(timezone.now(), "Y-m-d_H:i")}'
        )


class DeviceModelTests(TestCase):
    """ Tests for Device's model """

    model = Device

    @classmethod
    def setUpTestData(cls) -> None:
        # The device model has obligatory field - foreign key to the user model.
        # So, we need to create a user object model for testing the device model.
        user = SmsUser.objects.create_user(name='user', password='user')
        Device.objects.create(
            name='test_device',
            ip_fqdn='1.1.1.1',
            check_interval=5,
            updated_by=user
        )

    def test_get_absolute_url(self) -> None:
        device = self.model.objects.get(name='test_device')
        self.assertEqual(device.get_absolute_url(), '/sms/device/detail/test_device/')

    def test_get_edit_url(self) -> None:
        device = self.model.objects.get(name='test_device')
        self.assertEqual(device.get_edit_url(), '/sms/device/edit/test_device/')

    def test_get_delete_url(self) -> None:
        device = self.model.objects.get(name='test_device')
        self.assertEqual(device.get_delete_url(), '/sms/device/delete/test_device/')

    def test_set_status_valid(self) -> None:
        # The status must be a boolean
        device = self.model.objects.get(name='test_device')
        self.assertFalse(device.status)

        device.set_status(True)
        self.assertGreater(
            device.last_status_changed,
            timezone.now() - timezone.timedelta(minutes=1)
        )
        self.assertTrue(device.status)

    def test_set_status_invalid(self) -> None:
        # The status must be a boolean
        device = self.model.objects.get(name='test_device')
        self.assertFalse(device.status)
        with self.assertRaises(ValueError):
            device.set_status('UP')
