""" API serializers for the application sms_core """

from rest_framework import serializers

from sms_core.models import Device


class DeviceSerializer(serializers.ModelSerializer):
    """ A serializer for devices """

    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Device
        fields = ('__all__')
        read_only_fields = ('status', 'last_status_changed')


class DeviceUpdateSerializer(DeviceSerializer):
    """ A serializer for update devices """

    class Meta:
        model = Device
        fields = ('__all__')
        read_only_fields = ('name', 'status', 'last_status_changed')
