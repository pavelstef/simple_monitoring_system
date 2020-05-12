"""sms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .views import redirect_sms_login, redirect_sms_overview


urlpatterns = [
    path('', redirect_sms_overview),
    path('admin/', admin.site.urls),
    path('accounts/login/', redirect_sms_login),
    path('sms/', include('sms_core.urls')),
    path('api/v1/auth-base/', include('rest_framework.urls')),
    path('api/v1/auth-token/', include('djoser.urls.authtoken')),
    path('api/v1/sms/', include('sms_api.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
