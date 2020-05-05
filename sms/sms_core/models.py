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
    groups = None
    user_permissions = None

    # We will use if as slug.
    name = models.SlugField(max_length=50, unique=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    objects = SmsUserManager()

    def __str__(self) -> str:
        return str(self.name)

    def get_absolute_url(self) -> str:
        """ Get absolute URL to edit model's instance """
        return reverse('url_user_edit', kwargs={'slug': self.name})

    def get_delete_url(self) -> str:
        """ Get absolute URL to delete model's instance """
        return reverse('url_user_dell', kwargs={'slug': self.name})

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

    # We will use name as a slug.
    name = models.SlugField(max_length=20, unique=True)

    ip_fqdn = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=255, blank=True)
    status = models.BooleanField(default=False)
    last_status_changed = models.DateTimeField(auto_now_add=True)
    check_interval = models.PositiveIntegerField(default=60)
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
        return reverse('url_device_detail', kwargs={'slug': self.name})

    def get_edit_url(self) -> str:
        """ Get absolute URL to edit model's instance """
        return reverse('url_device_edit', kwargs={'slug': self.name})

    def get_delete_url(self) -> str:
        """ Get absolute URL to delete model's instance """
        return reverse('url_device_dell', kwargs={'slug': self.name})

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
