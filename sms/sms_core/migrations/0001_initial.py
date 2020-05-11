# Generated by Django 3.0.5 on 2020-05-11 22:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.SlugField(help_text='The username must be 4-20 characters long, contain letters and numbers, and must not contain spaces, special characters, or emoji.', unique=True, verbose_name='Username')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'get_latest_by': '-updated_at',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(help_text='The device name must be 5-20 ASCII characters long, contain letters and numbers, and must not contain spaces, special characters, or emoji.', max_length=20, unique=True, verbose_name='Device name')),
                ('ip_fqdn', models.CharField(help_text='The IP / FQDN must be 5-30 ASCII characters long, contain letters and numbers, and must not contain spaces, special characters, or emoji.', max_length=30, unique=True, verbose_name='Device IP / FQDN')),
                ('description', models.CharField(blank=True, help_text='This field able to contains a description  up to 255 characters', max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('last_status_changed', models.DateTimeField(auto_now_add=True)),
                ('check_interval', models.PositiveIntegerField(choices=[(5, '5 minutes'), (10, '10 minutes'), (15, '15 minutes'), (30, '30 minutes'), (60, '60 minutes')], default=60, verbose_name='Check interval')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Device',
                'verbose_name_plural': 'Devices',
                'get_latest_by': '-last_status_changed',
            },
        ),
    ]
