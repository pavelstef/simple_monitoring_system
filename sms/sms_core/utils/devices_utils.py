""" Utilities that work with devices """


import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from sms_core.models import Device


def device_ping(device: object, count='3') -> object:
    """ Synchronous ping of a device """
    result = subprocess.run(['ping', '-c', count, device.ip_fqdn], check=False)
    if result.returncode == 0:
        del result
        return device


def check_device_status(devices_list: list, workers_limit=5) -> None:
    """
    Checking devices statuses in multiple threads
    and set the status in DB in synchronous.
    """
    devices_obj_list = []
    device_up_list = []
    for item in devices_list:
        devices_obj_list.append(Device.objects.get(name__iexact=item))

    with ThreadPoolExecutor(max_workers=workers_limit) as executor:
        future_ping = {
            executor.submit(device_ping, device): device for device in devices_obj_list
        }
        for future in as_completed(future_ping):
            device_up_list. append(future.result())

    if device_up_list:
        for device in devices_obj_list:
            if device in device_up_list:
                device.set_status(True)
            else:
                device.set_status(False)

    del devices_obj_list
    del device_up_list
