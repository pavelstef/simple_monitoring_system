""" Models for the application sms_core """


from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone, dateformat


from .managers import SmsUserManager


class SmsUser(AbstractUser):
    """ The model that describe of users of the monitoring System """
    email = None
    username = None
    first_name = None
    last_name = None

    class Meta:
        get_latest_by = '-updated_at'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    # We will use if as slug.
    name = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Username',
        help_text='The username must be 4-20 characters long, contain letters and numbers,'
                  ' and must not contain spaces, special characters, or emoji.'
    )
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    objects = SmsUserManager()

    def __str__(self) -> str:
        return str(self.name)

    def get_absolute_url(self) -> str:
        """ Get absolute URL to edit model's instance """
        return reverse('sms_core:url_user_edit', kwargs={'slug': self.name})

    def get_delete_url(self) -> str:
        """ Get absolute URL to delete model's instance """
        return reverse('sms_core:url_user_dell', kwargs={'slug': self.name})

    def set_deleted(self) -> None:
        """
        Set models' instance as deleted and,
        change username to avoid problem with creating new instance with the same name
        """
        self.name += f'_deleted_at_{dateformat.format(timezone.now(), "Y-m-d_H:i")}'
        self.is_active = False
        self.save()


class Device(models.Model):
    """ The model that describe of devices of the monitoring System """

    class Meta:
        get_latest_by = '-last_status_changed'
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'

    # We will use name as a slug.
    name = models.SlugField(
        max_length=20,
        unique=True,
        verbose_name='Device name',
        help_text='The device name must be 5-20 ASCII characters long, contain letters and numbers,'
                  ' and must not contain spaces, special characters, or emoji.'
    )
    ip_fqdn = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Device IP / FQDN',
        help_text='The IP / FQDN must be 5-30 ASCII characters long, contain letters and numbers,'
                  ' and must not contain spaces, special characters, or emoji.'
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        help_text='This field able to contains a description  up to 255 characters'
    )
    status = models.BooleanField(default=False)
    last_status_changed = models.DateTimeField(auto_now_add=True)

    CHECK_INTERVALS = (
        (5, '5 minutes'), (10, '10 minutes'), (15, '15 minutes'),
        (30, '30 minutes'), (60, '60 minutes')
    )
    check_interval = models.PositiveIntegerField(
        choices=CHECK_INTERVALS,
        default=60,
        verbose_name='Check interval'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    # Audit trail
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    def __str__(self) -> str:
        return str(self.name)

    def get_absolute_url(self) -> str:
        """ Get absolute URL to show model's instance details """
        return reverse('sms_core:url_device_detail', kwargs={'slug': self.name})

    def get_edit_url(self) -> str:
        """ Get absolute URL to edit model's instance """
        return reverse('sms_core:url_device_edit', kwargs={'slug': self.name})

    def get_delete_url(self) -> str:
        """ Get absolute URL to delete model's instance """
        return reverse('sms_core:url_device_dell', kwargs={'slug': self.name})

    def set_status(self, status: bool) -> None:
        """
        Setting model's instance status:
        True - UP, reachable
        False - DOWN, unreachable
        """
        if isinstance(status, bool):
            if status != self.status:
                self.status = status
                self.last_status_changed = timezone.now()
                self.save()
        else:
            raise ValueError('The status must be boolean')
