"""
A base command to create default admin user
"""

from os import environ

from django.core.management import BaseCommand

from sms_core.models import SmsUser

USERNAME = environ.get('USERNAME', 'admin')
PASSWORD = environ.get('PASSWORD', 'password')


class Command(BaseCommand):

    def handle(self, *args, **options):
        if SmsUser.objects.count() == 0:
            print(f'Creating account for user {USERNAME}')
            admin = SmsUser.objects.create_superuser(name=USERNAME, password=PASSWORD)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
