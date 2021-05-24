""" Tests of using common API methods for unauthorized user """

from rest_framework.test import APITestCase

from sms_core.models import SmsUser, Device


class APICommonTests(APITestCase):
    """ A class which prepare data for tests """

    @classmethod
    def setUpTestData(cls) -> None:
        admin = SmsUser.objects.create_superuser(
            name='test_admin', password='test_admin'
        )
        admin.save()
        user = SmsUser.objects.create_user(
            name='test_user', password='test_user')
        user.save()
        Device.objects.create(
            pk=1,
            name='device1',
            ip_fqdn='1.1.1.1',
            description='Device 1 description',
            updated_by=admin
        )
        Device.objects.create(
            pk=2,
            name='device2',
            ip_fqdn='2.2.2.2',
            updated_by=admin
        )


class APICommonTestsAdmin(APICommonTests):
    """ A class which contains Tests of using common API methods for unauthorized admin """

    def setUp(self):
        self.client.login(username='test_admin', password='test_admin')

    def tearDown(self) -> None:
        self.client.logout()

    def test_device_list(self) -> None:
        devices = Device.objects.all()
        response = self.client.get(path='/api/v1/sms/devices')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['devices']), 2)
        for i, _ in enumerate(devices):
            self.assertEqual(response.data['devices'][i]['name'], devices[i].name)
            self.assertEqual(response.data['devices'][i]['ip_fqdn'], devices[i].ip_fqdn)
            self.assertEqual(response.data['devices'][i]['description'], devices[i].description)
            self.assertEqual(
                response.data['devices'][i]['check_interval'],
                devices[i].check_interval
            )

    def test_device_detail(self, pk=1) -> None:
        device = Device.objects.get(pk=pk)
        response = self.client.get(path=f'/api/v1/sms/devices/{pk}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['device']['name'], device.name)
        self.assertEqual(response.data['device']['ip_fqdn'], device.ip_fqdn)
        self.assertEqual(response.data['device']['description'], device.description)
        self.assertEqual(int(response.data['device']['check_interval']), device.check_interval)

    def test_device_create(self) -> None:
        data = {
            "name": "device3",
            "ip_fqdn": "3.3.3.3",
            "description": "Test device 3 description",
            "check_interval": "15"
        }
        response = self.client.post(path='/api/v1/sms/devices', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"success": "Device \"device3\" created successfully."}
        )
        new_device = Device.objects.get(name="device3")
        self.assertEqual(data.get('name'), new_device.name)
        self.assertEqual(data.get('ip_fqdn'), new_device.ip_fqdn)
        self.assertEqual(data.get('description'), new_device.description)
        self.assertEqual(int(data.get('check_interval')), new_device.check_interval)

    def test_device_update(self, pk=2) -> None:
        data = {
            "ip_fqdn": "33.33.33.33",
            "description": "Test device 3 NEW description",
            "check_interval": "30"
        }
        response = self.client.patch(path=f'/api/v1/sms/devices/{pk}', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"success": f"Device with id \"{pk}\" updated successfully."}
        )
        updated_device = Device.objects.get(pk=pk)
        self.assertEqual(data.get('ip_fqdn'), updated_device.ip_fqdn)
        self.assertEqual(data.get('description'), updated_device.description)
        self.assertEqual(int(data.get('check_interval')), updated_device.check_interval)

    def test_device_delete(self, pk=2) -> None:
        response = self.client.delete(path=f'/api/v1/sms/devices/{pk}')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(
            response.data,
            {'message': f'Device with id \"{pk}\" has been deleted'}
        )
        with self.assertRaises(Device.DoesNotExist):
            Device.objects.get(pk=pk)


class APICommonTestsUser(APICommonTests):
    """ A class which contains Tests of using common API methods for unauthorized user """

    def setUp(self):
        self.client.login(username='test_user', password='test_user')

    def tearDown(self) -> None:
        self.client.logout()

    def test_device_list(self) -> None:
        devices = Device.objects.all()
        response = self.client.get(path='/api/v1/sms/devices')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['devices']), 2)
        for i, _ in enumerate(devices):
            self.assertEqual(response.data['devices'][i]['name'], devices[i].name)
            self.assertEqual(response.data['devices'][i]['ip_fqdn'], devices[i].ip_fqdn)
            self.assertEqual(response.data['devices'][i]['description'], devices[i].description)
            self.assertEqual(
                response.data['devices'][i]['check_interval'],
                devices[i].check_interval
            )

    def test_device_detail(self, pk=1) -> None:
        device = Device.objects.get(pk=pk)
        response = self.client.get(path=f'/api/v1/sms/devices/{pk}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['device']['name'], device.name)
        self.assertEqual(response.data['device']['ip_fqdn'], device.ip_fqdn)
        self.assertEqual(response.data['device']['description'], device.description)
        self.assertEqual(int(response.data['device']['check_interval']), device.check_interval)

    def test_device_create(self) -> None:
        data = {
            "name": "device3",
            "ip_fqdn": "3.3.3.3",
            "description": "Test device 3 description",
            "check_interval": "15"
        }
        response = self.client.post(path='/api/v1/sms/devices', data=data)
        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"detail": "You do not have permission to perform this action."}
        )

    def test_device_update(self, pk=2) -> None:
        data = {
            "ip_fqdn": "33.33.33.33",
            "description": "Test device 3 NEW description",
            "check_interval": "30"
        }
        response = self.client.patch(path=f'/api/v1/sms/devices/{pk}', data=data)
        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"detail": "You do not have permission to perform this action."}
        )

    def test_device_delete(self, pk=2) -> None:
        response = self.client.delete(path=f'/api/v1/sms/devices/{pk}')
        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"detail": "You do not have permission to perform this action."}
        )
