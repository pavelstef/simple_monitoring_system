""" Forms of the application sms_core """

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import SmsUser, Device


class UserCreationForm(forms.ModelForm):
    """ A Form that validates data for creating User object """
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': "Password",
                'required': True,
                'minlength': "3",
                'maxlength': "20"}))
    password2 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': "Password",
                'required': True,
                'minlength': "3",
                'maxlength': "20"}))

    class Meta:
        model = SmsUser
        fields = ['name', 'is_staff']

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': "Username",
                    'required': True,
                    'minlength': "3",
                    'maxlength': "20"}),
            'is_staff': forms.CheckboxInput(
                attrs={'class': "form-check-input"}),
        }

    def clean_name(self):
        new_name = self.cleaned_data.get('name')

        if new_name.lower() in ['create', 'add', 'edit']:
            raise ValidationError('Please, use other username')

        if SmsUser.objects.filter(name__iexact=new_name).count():
            raise ValidationError(
                f'name must be unique. We have "{new_name}" already')

        return new_name

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """ A Form that validates data for changing User data """
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': "Password",
                'required': True,
                'minlength': "3",
                'maxlength': "20"}))
    password2 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': "Password",
                'required': True,
                'minlength': "3",
                'maxlength': "20"}))

    class Meta:
        model = SmsUser
        fields = ['name']

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': "Username",
                    'required': True,
                    'minlength': "3",
                    'maxlength': "20",
                    'readonly': True})}

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        name = self.cleaned_data.get('name')
        if name:
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

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': "Device name",
                    'required': True,
                    'minlength': "5",
                    'maxlength': "20"}),
            'ip_fqdn': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': "IP / FQDN",
                    'required': True,
                    'minlength': "5",
                    'maxlength': "20"}),
            'description': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': "Description",
                    'maxlength': "250"}),
            'check_interval': forms.NumberInput(
                attrs={
                    'class': "form-control",
                    'min': "5",
                    'max': "60",
                    'step': "5"}),
        }

    def clean_name(self):
        new_name = self.cleaned_data.get('name')
        if new_name.lower() in ['create', 'add', 'edit']:
            raise ValidationError('Please, use other name')
        return new_name

    def clean_check_interval(self):
        new_check_interval = self.cleaned_data.get('check_interval')
        if new_check_interval < 5 or (new_check_interval % 5) != 0:
            raise ValidationError(
                'Check interval should be multiple of 5 minutes')
        return new_check_interval

    def clean_updated_at(self):
        return timezone.now()

    def save(self, commit=True):
        # Set an updated_at field on update
        device = super().save(commit=False)
        device.updated_at = timezone.now()
        if commit:
            device.save()
        return device
