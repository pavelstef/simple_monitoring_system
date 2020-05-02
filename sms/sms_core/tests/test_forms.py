""" Tests for sms_core forms. """

from django.test import TestCase
from sms_core.forms import UserCreationForm, UserChangeForm, DeviceForm
from sms_core.models import SmsUser, Device


class UserCreationFormTests(TestCase):
    """ Tests for UserCreationForm """

    form = UserCreationForm

    @classmethod
    def setUpTestData(cls):
        SmsUser.objects.create_user(name='test_user', password='test_password')

    def test_form_name_label(self):
        self.assertEqual(self.form().fields['name'].label, 'Username:')

    def test_form_name_invalid(self):
        # 'create', 'add', 'edit' - these names are not valid
        form_data = {'name': 'create', 'password1': 'test_password',
                     'password2': 'test_password'}
        form = self.form(data=form_data)
        self.assertFalse(form.is_valid())
        form_data = {'name': 'add', 'password1': 'test_password',
                     'password2': 'test_password'}
        form = self.form(data=form_data)
        self.assertFalse(form.is_valid())
        form_data = {'name': 'edit', 'password1': 'test_password',
                     'password2': 'test_password'}
        form = self.form(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_name_duplicate(self):
        form_data = {'name': 'test_user', 'password1': 'test_password',
                     'password2': 'test_password'}
        form = self.form(data=form_data)
        self.assertFalse(form.is_valid())
        form_data = {'name': 'another_user', 'password1': 'test_password',
                     'password2': 'test_password'}
        form = self.form(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_password1_label(self):
        self.assertEqual(self.form().fields['password1'].label, 'Password:')

    def test_form_password2_label(self):
        self.assertEqual(
            self.form().fields['password2'].label,
            'Confirm password:')

    def test_form_password_match(self):
        form_data = {'name': 'some_name', 'password1': 'test_password',
                     'password2': 'test_password1'}
        form = self.form(data=form_data)
        self.assertFalse(form.is_valid())
        form_data = {'name': 'some_name', 'password1': 'test_password',
                     'password2': 'test_password'}
        form = self.form(data=form_data)
        self.assertTrue(form.is_valid())


class UserChangeFormTests(TestCase):
    """ Tests for UserChangeForm """

    form = UserChangeForm

    def test_form_password1_label(self):
        self.assertEqual(
            self.form().fields['password1'].label,
            'New password:')

    def test_form_password2_label(self):
        self.assertEqual(
            self.form().fields['password2'].label,
            'Confirm password:')

    def test_form_password_match(self):
        form_data = {'name': 'some_name', 'password1': 'test_password',
                     'password2': 'test_password1'}
        form = self.form(data=form_data)
        self.assertFalse(form.is_valid())
        form_data = {'name': 'some_name', 'password1': 'test_password',
                     'password2': 'test_password'}
        form = self.form(data=form_data)
        self.assertTrue(form.is_valid())


class DeviceFormTests(TestCase):
    """ Tests for DeviceForm """

    form = DeviceForm

    @classmethod
    def setUpTestData(cls):
        # The device model has obligatory field - foreign key to the user model.
        # So, we need to create a user object model for testing the device
        # model.
        SmsUser.objects.create_user(name='user', password='user')
        user = SmsUser.objects.get(name='user')
        Device.objects.create(
            name='test_device',
            ip_fqdn='1.1.1.1',
            check_interval=5,
            updated_by=user
        )

    def test_form_name_label(self):
        self.assertEqual(self.form().fields['name'].label, 'Device name:')

    def test_form_name_invalid(self):
        # 'create', 'add', 'edit' - these names are not valid
        form_data = {'name': 'create', 'ip_fqdn': '2.2.2.2',
                     'check_interval': '5'}
        form = self.form(data=form_data)
        self.assertFalse(form.is_valid())
        form_data = {'name': 'add', 'ip_fqdn': '2.2.2.2',
                     'check_interval': '5'}
        form = self.form(data=form_data)
        self.assertFalse(form.is_valid())
        form_data = {'name': 'edit', 'ip_fqdn': '2.2.2.2',
                     'check_interval': '5'}
        form = self.form(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_name_duplicate(self):
        form_data = {'name': 'test_device', 'ip_fqdn': '2.2.2.2',
                     'check_interval': '5'}
        form = self.form(data=form_data)
        self.assertFalse(form.is_valid())
        form_data = {'name': 'another_device', 'ip_fqdn': '2.2.2.2',
                     'check_interval': '5'}
        form = self.form(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_ip_fqdn_label(self):
        self.assertEqual(
            self.form().fields['ip_fqdn'].label,
            'Device IP / FQDN:'
        )

    def test_form_description_label(self):
        self.assertEqual(
            self.form().fields['description'].label,
            'Description:'
        )

    def test_form_check_interval_label(self):
        self.assertEqual(
            self.form().fields['check_interval'].label,
            'Check interval (minutes):'
        )

    def test_form_check_interval_invalid(self):
        # Less than 5 or not a multiple of 5
        form_data = {'name': 'some_device', 'ip_fqdn': '3.3.3.3',
                     'check_interval': '1'}
        form = self.form(data=form_data)
        self.assertFalse(form.is_valid())
        form_data = {'name': 'some_device', 'ip_fqdn': '3.3.3.3',
                     'check_interval': '13'}
        form = self.form(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_check_interval_valid(self):
        # More than 5 and multiple of 5
        form_data = {'name': 'some_device', 'ip_fqdn': '3.3.3.3',
                     'check_interval': '10'}
        form = self.form(data=form_data)
        self.assertTrue(form.is_valid())
