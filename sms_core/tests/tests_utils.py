""" Tests for sms_core utils. """

from django.test import TestCase

from sms_core.models import SmsUser, Device
from sms_core.utils.devices_utils import device_ping, check_device_status


class DeviceUtilsTests(TestCase):
    """ Tests for the device utils """

    @classmethod
    def setUpTestData(cls) -> None:
        # The device model has obligatory field - foreign key to the user model.
        # So, we need to create a user object model for testing the device
        # model.
        user = SmsUser.objects.create_user(name='user', password='user')
        Device.objects.create(
            name='device1',
            ip_fqdn='127.0.0.1',  # Pingable
            check_interval=5,
            updated_by=user
        )
        Device.objects.create(
            name='device2',
            ip_fqdn='localhost',  # Pingable
            check_interval=5,
            updated_by=user
        )
        Device.objects.create(
            name='device3',
            ip_fqdn='128.0.0.1',  # Unpingable
            check_interval=5,
            updated_by=user
        )
        Device.objects.create(
            name='device4',
            ip_fqdn='not_localhost',  # Unpingable
            check_interval=5,
            updated_by=user
        )

    def test_device_ping(self) -> None:
        all_devices = Device.objects.all()
        up_devices = []
        for device in all_devices:
            if device_ping(device):
                up_devices.append(device)
        self.assertEqual(up_devices, all_devices[:2])

    def test_check_device_status(self) -> None:
        all_devices_names = []
        for device in Device.objects.all():
            all_devices_names.append(device.name)
        check_device_status(all_devices_names)
        self.assertTrue(Device.objects.get(name='device1').status)
        self.assertTrue(Device.objects.get(name='device2').status)
        self.assertFalse(Device.objects.get(name='device3').status)
        self.assertFalse(Device.objects.get(name='device4').status)
