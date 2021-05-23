""" Tests of using common API methods for unauthorized user """

from rest_framework.test import APISimpleTestCase


class APICommonTests(APISimpleTestCase):
    """ A class which contains Tests of using common API methods for unauthorized user """

    def test_device_list(self) -> None:
        response = self.client.get(path='/api/v1/sms/devices')
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"detail": "Authentication credentials were not provided."}
        )

    def test_device_detail(self, pk=1) -> None:
        response = self.client.get(path=f'/api/v1/sms/devices/{pk}')
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"detail": "Authentication credentials were not provided."}
        )

    def test_device_create(self) -> None:
        data = {
            "name": "test_device1",
            "ip_fqdn": "127.0.0.1",
            "description": "Test device 1 description",
            "check_interval": "5"
        }
        response = self.client.post(path='/api/v1/sms/devices', data=data)
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"detail": "Authentication credentials were not provided."}
        )

    def test_device_update(self, pk=1) -> None:
        data = {
            "ip_fqdn": "127.0.0.2",
            "description": "Test device 2 description",
            "check_interval": "10"
        }
        response = self.client.patch(path=f'/api/v1/sms/devices/{pk}', data=data)
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"detail": "Authentication credentials were not provided."}
        )

    def test_device_delete(self, pk=1) -> None:
        response = self.client.delete(path=f'/api/v1/sms/devices/{pk}')
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"detail": "Authentication credentials were not provided."}
        )
