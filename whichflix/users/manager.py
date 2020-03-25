from whichflix.users.models import Device


def get_or_create_device(device_token: str) -> Device:
    try:
        device = Device.objects.get(device_token=device_token)
    except Device.DoesNotExist:
        device = _create_device(device_token)

    return device


def _create_device(device_token: str) -> Device:
    device = Device.objects.create(device_token=device_token)

    return device
