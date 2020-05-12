""" Registration data models in the admin panel """

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import SmsUser, Device
from .forms import UserCreationForm, UserChangeForm


class SmsUserAdmin(UserAdmin):
    """ A custom user's model for a Django admin site """
    add_form = UserCreationForm
    form = UserChangeForm
    model = SmsUser
    list_display = ('name', 'is_staff', 'is_active',)
    list_filter = ('name', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('name', 'password')}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'password1', 'password2', 'is_staff',)}
         ),
    )
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(SmsUser, SmsUserAdmin)
admin.site.register(Device)
