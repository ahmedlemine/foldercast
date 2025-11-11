import pytz
from datetime import datetime
from django.conf import settings

def get_timezone_aware_datetime(timestamp):
    creation_datetime = datetime.fromtimestamp(timestamp)
    target_timezone = pytz.timezone(settings.TIME_ZONE)
    tz_aware_datetime = target_timezone.localize(creation_datetime)
    return tz_aware_datetime


def build_host(request):
    host = request.get_host()
    if settings.DEBUG:
        return host
    return f"{host}:{settings.SERVER_PORT}"