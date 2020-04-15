""" sms_core URL Configuration """


from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.SmsLogInView.as_view(), name='url_login'),
    path('logout/', views.SmsLogOutView.as_view(), name='url_logout'),
    path('overview/', views.SmsOverviewView.as_view(), name='url_devices_overview'),
    path('administration/', views.SmsAdministrationView.as_view(), name='url_administration'),
    path('user/create/', views.SmsUserCreateView.as_view(), name='url_user_create'),
    path('user/edit/<str:slug>/', views.SmsUserEditView.as_view(), name='url_user_edit'),
    path('user/delete/<str:slug>/', views.SmsUserDeleteView.as_view(), name='url_user_dell'),
    path('device/add/', views.SmsDeviceAddView.as_view(), name='url_device_add'),
    path('device/edit/<str:slug>/', views.SmsDeviceEditView.as_view(), name='url_device_edit'),
    path('device/detail/<str:slug>/', views.SmsDeviceDetailsView.as_view(), name='url_device_detail'),
    path('device/delete/<str:slug>/', views.SmsDeviceDeleteView.as_view(), name='url_device_dell'),
]
