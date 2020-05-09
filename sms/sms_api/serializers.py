""" API serializers for the application sms_core """

from rest_framework import serializers

from sms_core.models import Device


class DeviceCreateEditSerializer(serializers.ModelSerializer):
    """ A serializer for create or edit devices """

    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Device
        fields = ('name', 'ip_fqdn', 'description', 'check_interval', 'updated_by')


class DeviceViewSerializer(serializers.ModelSerializer):
    """ A serializer for show device details """

    class Meta:
        model = Device
        fields = ('id', 'name', 'ip_fqdn', 'description', 'status', 'last_status_changed',
                  'check_interval')
