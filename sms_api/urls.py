""" sms_api URL Configuration """

from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from .views import DeviceView

router = DefaultRouter(trailing_slash=False)
router.register(r'devices', DeviceView, basename='device')
urlpatterns = router.urls

doc_urlpatterns = [
    path('docs/', include_docs_urls(title='Simple Monitoring System REST API'))
]

urlpatterns += doc_urlpatterns
