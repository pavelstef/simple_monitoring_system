""" Views of REST API interface """

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from sms_core.models import Device
from .serializers import DeviceCreateEditSerializer, DeviceViewSerializer


class DeviceCreateView(generics.CreateAPIView):
    """ A View to create a device """
    permission_classes = (IsAdminUser,)
    serializer_class = DeviceCreateEditSerializer


class DeviceEditDeletelView(generics.RetrieveUpdateDestroyAPIView):
    """ A View to edit or delete a device """
    permission_classes = (IsAdminUser,)
    serializer_class = DeviceCreateEditSerializer
    queryset = Device.objects.all()


class DevicesListView(generics.ListAPIView):
    """ A View to show list of all devices """
    permission_classes = (IsAuthenticated,)
    serializer_class = DeviceViewSerializer
    queryset = Device.objects.all()


class DeviceDetailView(generics.RetrieveAPIView):
    """ A View to show details about a specific device """
    permission_classes = (IsAuthenticated,)
    serializer_class = DeviceViewSerializer
    queryset = Device.objects.all()
