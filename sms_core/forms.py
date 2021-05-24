""" Forms of the application sms_core """

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import SmsUser, Device


class UserCreationForm(forms.ModelForm):
    """ A Form that validates data for creating User object """

    passwords_help_text = 'The password must be 8-20 characters long, contain letters and numbers, ' \
                          'and must not contain spaces, special characters, or emoji.'

    password1 = forms.CharField(
        label='Password',
        help_text=passwords_help_text,
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': "Password",
                'required': True,
                'minlength': "8",
                'maxlength': "20"}))
    password2 = forms.CharField(
        label='Confirm password',
        help_text=passwords_help_text,
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': "Password",
                'required': True,
                'minlength': "8",
                'maxlength': "20"}))

    class Meta:
        model = SmsUser
        fields = ['name', 'is_staff']
        labels = {
            'is_staff': "Grant user administrator's permission?"
        }
        error_messages = {
            'name': {
                'invalid': 'Enter a valid “Username” consisting of letters, numbers,'
                           ' underscores or hyphens.'
            }
        }

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': "Username",
                    'minlength': "4",
                    'maxlength': "20"}),
            'is_staff': forms.CheckboxInput(
                attrs={'class': "form-check-input"}),
        }

    def clean_name(self) -> str:
        new_name = self.cleaned_data.get('name')

        if new_name.lower() in ['create', 'add', 'edit']:
            raise ValidationError('Please, use other username')

        if SmsUser.objects.filter(name__iexact=new_name).count():
            raise ValidationError(
                f'name must be unique. We have "{new_name}" already')

        return new_name

    def clean_password2(self) -> str:
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True) -> object:
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(UserCreationForm):
    """ A Form that validates data for changing User data """

    class Meta:
        model = SmsUser
        fields = ['name']

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': "Username",
                    'minlength': "4",
                    'maxlength': "20",
                    'readonly': True})}

    def clean_name(self) -> str:
        name = self.cleaned_data.get('name')
        return name

    def save(self, commit=True) -> object:
        # Save the provided password in hashed format
        name = self.cleaned_data.get('name')
        user = SmsUser.objects.get(name__iexact=name)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user


class DeviceForm(forms.ModelForm):
    """ A Form that validates data for a Device object """
    # updated_at = forms.DateTimeField()

    class Meta:
        model = Device
        fields = ['name', 'ip_fqdn', 'description', 'check_interval']
        error_messages = {
            'name': {
                'invalid': 'Enter a valid “Device name” consisting of letters, numbers,'
                           ' underscores or hyphens.'
            }
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': "Device name",
                    'minlength': "5",
                    'maxlength': "20"}),
            'ip_fqdn': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': "IP / FQDN",
                    'minlength': "5",
                    'maxlength': "30"}),
            'description': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': "Description",
                    'maxlength': "255"})
        }

    def clean_name(self) -> str:
        new_name = self.cleaned_data.get('name')
        if new_name.lower() in ['create', 'add', 'edit']:
            raise ValidationError('Please, use other name')
        return new_name

    def clean_updated_at(self) -> str:
        return timezone.now()

    def save(self, commit=True) -> object:
        # Set an updated_at field on update
        device = super().save(commit=False)
        device.updated_at = timezone.now()
        if commit:
            device.save()
        return device
