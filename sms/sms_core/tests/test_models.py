""" Tests for sms_core models. """

from django.test import TestCase
from django.utils import timezone, dateformat
from sms_core.models import SmsUser, Device


class SmsUserModelTest(TestCase):
    """ Test for custom user model SmsUser """

    @classmethod
    def setUpTestData(cls):
        SmsUser.objects.create_superuser(
            name='test_admin', password='test_admin'
        )
        SmsUser.objects.create_user(name='test_user', password='test_user')

    def test_name_label(self):
        admin = SmsUser.objects.get(name='test_admin')
        user = SmsUser.objects.get(name='test_user')
        field_label_admin = admin._meta.get_field('name').verbose_name
        field_label_user = user._meta.get_field('name').verbose_name
        self.assertEqual(field_label_admin, 'name')
        self.assertEqual(field_label_user, 'name')

    def test_get_absolute_url(self):
        admin = SmsUser.objects.get(name='test_admin')
        user = SmsUser.objects.get(name='test_user')
        self.assertEqual(admin.get_absolute_url(), '/sms/user/edit/test_admin/')
        self.assertEqual(user.get_absolute_url(), '/sms/user/edit/test_user/')

    def test_get_delete_url(self):
        admin = SmsUser.objects.get(name='test_admin')
        user = SmsUser.objects.get(name='test_user')
        self.assertEqual(admin.get_delete_url(), '/sms/user/delete/test_admin/')
        self.assertEqual(user.get_delete_url(), '/sms/user/delete/test_user/')

    def test_set_deleted(self):
        admin = SmsUser.objects.get(name='test_admin')
        user = SmsUser.objects.get(name='test_user')
        admin.set_deleted()
        user.set_deleted()
        self.assertFalse(admin.is_active)
        self.assertFalse(user.is_active)
        self.assertEqual(
            admin.name,
            f'test_admin_deleted_at_{dateformat.format(timezone.now(), "Y-m-d_H:i")}'
        )
        self.assertEqual(
            user.name,
            f'test_user_deleted_at_{dateformat.format(timezone.now(), "Y-m-d_H:i")}'
        )


class DeviceModelTest(TestCase):
    """ Tests for Device's model """

    @classmethod
    def setUpTestData(cls):
        # The device model has obligatory field - foreign key to the user model.
        # So, we need to create a user object model for testing the device model.
        SmsUser.objects.create_user(name='user', password='user')
        user = SmsUser.objects.get(name='user')
        Device.objects.create(
            name='test_device',
            ip_fqdn='1.1.1.1',
            updated_by=user
        )

    def test_name_label(self):
        device = Device.objects.get(name='test_device')
        field_label = device._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_get_absolute_url(self):
        device = Device.objects.get(name='test_device')
        self.assertEqual(device.get_absolute_url(), '/sms/device/detail/test_device/')

    def test_get_edit_url(self):
        device = Device.objects.get(name='test_device')
        self.assertEqual(device.get_edit_url(), '/sms/device/edit/test_device/')

    def test_get_delete_url(self):
        device = Device.objects.get(name='test_device')
        self.assertEqual(device.get_delete_url(), '/sms/device/delete/test_device/')

    def test_set_status(self):
        device = Device.objects.get(name='test_device')
        self.assertFalse(device.status)
        device.set_status(True)
        self.assertGreater(
            device.last_status_changed,
            timezone.now() - timezone.timedelta(minutes=1)
        )
        self.assertTrue(device.status)
        with self.assertRaises(ValueError):
            device.set_status('UP')
