import pytz
from datetime import datetime
import validators
from django.conf import settings


def get_timezone_aware_datetime(timestamp):
    creation_datetime = datetime.fromtimestamp(timestamp)
    target_timezone = pytz.timezone(settings.TIME_ZONE)
    tz_aware_datetime = target_timezone.localize(creation_datetime)
    return tz_aware_datetime


def build_host(request):
    base_host = request.get_host()
    protocol = request.scheme
    host_with_protocol = f"{protocol}://{base_host}"

    # if using a domain name, don't add a port number
    if validators.domain(base_host):
        return host_with_protocol

    return f"{host_with_protocol}:{settings.SERVER_PORT}"
