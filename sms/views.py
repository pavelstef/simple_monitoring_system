""" Project's core views """


from django.shortcuts import redirect


def redirect_sms_overview(request):
    """ Permanent redirect to a homepage of the monitoring system """
    return redirect('sms_core:url_devices_overview', permanent=True)


def redirect_sms_login(request):
    """ Permanent redirect to a login page """
    return redirect('sms_core:url_login', permanent=True)
