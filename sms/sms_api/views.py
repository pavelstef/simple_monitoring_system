"""
Views of REST API interface.
I use a ViewSet instead a ModelViewSet to do customisation of responses
"""

from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from sms_core.models import Device
from .serializers import DeviceSerializer, DeviceUpdateSerializer


class DeviceView(viewsets.ViewSet):
    """
    A REST API class that contains methods for working with devices: GET, PUT, PATCH, DELETE
    """

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ('list', 'retrieve'):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request):
        """ Getting information about all devices. GET method """
        queryset = Device.objects.all()
        serializer = DeviceSerializer(queryset, many=True)
        return Response({'devices': serializer.data})

    def create(self, request):
        """ Creating a new device. POST method """
        serializer = DeviceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            device_saved = serializer.save()
        return Response({'success': f'Device "{device_saved.name}" created successfully.'})

    def retrieve(self, request, pk=None):
        """ Getting information about  a specific device. GET method """
        queryset = Device.objects.all()
        device = get_object_or_404(queryset, pk=pk)
        serializer = DeviceSerializer(device)
        return Response({'device': serializer.data})

    def partial_update(self, request, pk=None):
        """ Updating device properties. PATCH method """
        queryset = Device.objects.all()
        device = get_object_or_404(queryset, pk=pk)
        serializer = DeviceUpdateSerializer(
            device, data=request.data,
            context={'request': request},
            partial=True
        )
        if serializer.is_valid(raise_exception=True):
            device_saved = serializer.save()
        return Response({'success': f'Device with id "{pk}" updated successfully.'})

    def destroy(self, request, pk=None):
        """ Removing a device. DELETE method """
        queryset = Device.objects.all()
        device = get_object_or_404(queryset, pk=pk)
        device.delete()
        return Response({'message': f'Device with id "{pk}" has been deleted'}, status=204)
