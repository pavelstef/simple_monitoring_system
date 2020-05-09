""" sms_api URL Configuration """


from django.urls import path

from . import views

app_name = 'sms_api'

urlpatterns = [
    path('devices/create/', views.DeviceCreateView.as_view(), name='url_device_create'),
    path('devices/all/', views.DevicesListView.as_view(), name='url_device_list'),
    path('devices/<int:pk>/', views.DeviceEditDeletelView.as_view(), name='url_device_edit'),
    path('devices/detail/<int:pk>/', views.DeviceDetailView.as_view(), name='url_device_detail'),
]
