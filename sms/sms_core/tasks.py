""" Celery tasks """


from celery.signals import worker_ready
from sms.celery import celery_app

from .utils.devices_utils import check_device_status
from .models import Device


DEVICES = {}


@worker_ready.connect
def task_initial_device_check(**kwargs) -> None:
    """ Checking all devices after the Celery initiation """
    devices_for_checking = []
    devices = Device.objects.all()
    if devices:
        for device in devices:
            devices_for_checking.append(device.name)
        check_device_status(devices_for_checking)
    del devices_for_checking
    del devices


@celery_app.task(time_limit=20, default_retry_delay=5, max_retries=2)
def task_device_check_after_update(device_name: str) -> None:
    """ Checking the device after update properties """
    new_device = Device.objects.filter(name__iexact=device_name)[0]
    check_device_status([new_device.name], workers_limit=1)
    del new_device


@celery_app.task(time_limit=200, max_retries=1)
def task_device_check_loop(global_device_dict=DEVICES, loop_time=5) -> None:
    """ Devices monitoring loop """
    devices_for_checking = []
    devices_for_removing = []

    # Checking the database to find new devices
    devices_query_set = Device.objects.all()

    # Devices that are not exists in the database we select for removing
    if global_device_dict:
        for device in global_device_dict.keys():
            if device not in [d.name for d in devices_query_set]:
                devices_for_removing.append(device)
        if devices_for_removing:
            for device in devices_for_removing:
                global_device_dict.pop(device)

    if devices_query_set:

        # Decreasing countdown timer for devices that were found or already
        # existed
        for device in devices_query_set:
            if device.name not in global_device_dict.keys():
                global_device_dict[device.name] = device.check_interval - loop_time
            else:
                if device.check_interval < global_device_dict[device.name]:
                    global_device_dict[device.name] = device.check_interval - loop_time
                global_device_dict[device.name] -= loop_time

        # Devices whose timer has expired, we select for checking
        if global_device_dict:
            for device_name, countdown_timer in global_device_dict.items():
                if countdown_timer <= 0:
                    devices_for_checking.append(device_name)
        if devices_for_checking:
            for device in devices_for_checking:
                global_device_dict.pop(device)
            check_device_status(devices_for_checking)

    del devices_for_checking
    del devices_for_removing
    del devices_query_set
