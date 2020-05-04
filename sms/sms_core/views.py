""" Views of the application sms_core """


from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout

from .models import SmsUser, Device
from .forms import DeviceForm, UserCreationForm, UserChangeForm
from .tasks import task_device_check_after_update


class ObjectDetailMixin:
    """ Mixin class to get any object's details """
    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, name__iexact=slug)
        context = {self.model.__name__.lower(): obj}
        del obj
        return render(request, self.template, context=context)


class ObjectListMixin:
    """ Mixin class to get list of all object's """
    model = None
    template = None

    def get(self, request):
        search_query = request.GET.get('search', '')
        if search_query:
            objs = self.model.objects.filter(name__icontains=search_query)
        else:
            if self.model == SmsUser:
                # Getting only active users.
                objs = self.model.objects.filter(is_active__iexact=1)
            else:
                objs = self.model.objects.all()
        context = {
            f'{self.model.__name__.lower()}s': objs,
            'search': search_query
        }
        del search_query
        del objs
        return render(request, self.template, context=context)


class ObjectCreateMixin:
    """ Mixin class to create some object """
    form_model = None
    template = None

    def get(self, request):
        form = self.form_model()
        context = {'form': form}
        del form
        return render(request, self.template, context)

    def post(self, request):
        context = {}
        bound_form = self.form_model(request.POST)

        if bound_form.is_valid():
            if self.form_model == DeviceForm:
                user = SmsUser.objects.get(name__iexact=request.user)
                complete_form = bound_form.save(commit=False)
                complete_form.updated_by = user
                complete_form.save()
                # Run Celery task
                task_device_check_after_update.delay((complete_form.name), )
                del user
                del complete_form
            else:
                bound_form.save()
            context.update({'form': self.form_model(), 'success': True})
        else:
            context.update({'form': bound_form, 'success': False})

        del bound_form
        return render(request, self.template, context=context)


class ObjectEditMixin:
    """ Mixin class to edit some object """
    model = None
    form_model = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(name__iexact=slug)
        bound_form = self.form_model(instance=obj)
        context = {
            'form': bound_form,
            'obj': obj
        }
        del obj
        del bound_form
        return render(request, self.template, context=context)

    def post(self, request, slug):
        obj = self.model.objects.get(name__iexact=slug)
        bound_form = self.form_model(request.POST, instance=obj)
        context = {'obj': obj}

        if bound_form.is_valid():
            if self.form_model == DeviceForm:
                user = SmsUser.objects.get(name__iexact=request.user)
                complete_form = bound_form.save(commit=False)
                complete_form.updated_by = user
                complete_form.save()
                # Run Celery task
                task_device_check_after_update.delay((complete_form.name), )
                del user
                del complete_form
            else:
                bound_form.save()
            context.update({'form': bound_form, 'success': True})
        else:
            context.update({'form': bound_form, 'success': False})

        del obj
        del bound_form
        return render(request, self.template, context=context)


class ObjectDeleteMixin:
    """ Mixin class to delete some object """
    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(name__iexact=slug)
        context = {
            'redirect_url': self.redirect_url,
            'obj': obj
        }
        del obj
        return render(request, self.template, context=context)

    def post(self, request, slug):
        obj = self.model.objects.get(name__iexact=slug)
        if isinstance(obj, SmsUser):
            # A user with administrator rights cannot be deleted if he is the
            # last one.
            if obj.is_staff and \
                    (self.model.objects.filter(is_active__iexact=1,
                                               is_staff__iexact=1).count() <= 1):
                pass
            else:
                obj.set_deleted()
        else:
            obj.delete()
        del obj
        return redirect(reverse(self.redirect_url))


class SmsLogInView(View):
    """ Custom View to login user """

    def get(self, request):
        return render(request, 'sms_core/sms_log_in.html',
                      {'message': 'Please, enter your username and password.'})

    def post(self, request):
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            del name
            del password
            return redirect(reverse('url_devices_overview'))

        del name
        del password
        return render(request, 'sms_core/sms_log_in.html',
                      {'message': 'Wrong username or password!'})


class SmsLogOutView(View):
    """ Custom View to logout user """

    def get(self, request):
        logout(request)
        return redirect(reverse('url_login'))


class SmsOverviewView(LoginRequiredMixin, ObjectListMixin, View):
    """ View to get list of all devices """
    model = Device
    template = 'sms_core/sms_overview.html'


class SmsAdministrationView(LoginRequiredMixin, ObjectListMixin, View):
    """ View to get list of all users """
    model = SmsUser
    template = 'sms_core/sms_administration.html'


class SmsDeviceDetailsView(LoginRequiredMixin, ObjectDetailMixin, View):
    """ View to get device's details """
    model = Device
    template = 'sms_core/sms_device_detail.html'


class SmsDeviceEditView(LoginRequiredMixin, ObjectEditMixin, View):
    """ View to edit device properties """
    model = Device
    form_model = DeviceForm
    template = 'sms_core/sms_device_edit.html'


class SmsUserCreateView(LoginRequiredMixin, ObjectCreateMixin, View):
    """ View to create new user """
    form_model = UserCreationForm
    template = 'sms_core/sms_user_create.html'


class SmsDeviceAddView(LoginRequiredMixin, ObjectCreateMixin, View):
    """ View to add new device """
    form_model = DeviceForm
    template = 'sms_core/sms_device_add.html'


class SmsDeviceDeleteView(LoginRequiredMixin, ObjectDeleteMixin, View):
    """ View to delete a device """
    model = Device
    template = 'sms_core/sms_confirmation.html'
    redirect_url = 'url_devices_overview'


class SmsUserDeleteView(LoginRequiredMixin, ObjectDeleteMixin, View):
    """ View to delete a user """
    model = SmsUser
    template = 'sms_core/sms_confirmation.html'
    redirect_url = 'url_administration'


class SmsUserEditView(LoginRequiredMixin, ObjectEditMixin, View):
    """ View to get users's details and edit self password """
    model = SmsUser
    form_model = UserChangeForm
    template = 'sms_core/sms_user_edit.html'

    def post(self, request, slug):
        obj = self.model.objects.get(name__iexact=slug)
        bound_form = self.form_model(request.POST, instance=obj)
        context = {'obj': obj}

        if bound_form.is_valid():
            bound_form.save()
            context.update({'form': bound_form, 'success': True})
        else:
            context.update({'form': bound_form, 'success': False})

        del obj
        del bound_form
        return render(request, self.template, context=context)
