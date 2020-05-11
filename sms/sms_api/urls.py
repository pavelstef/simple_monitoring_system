""" sms_api URL Configuration """

from rest_framework.routers import DefaultRouter

from .views import DeviceView

router = DefaultRouter(trailing_slash=False)
router.register(r'devices', DeviceView, basename='device')
urlpatterns = router.urls
