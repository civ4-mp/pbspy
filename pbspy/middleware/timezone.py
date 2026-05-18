from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from django.utils import timezone
from django.conf import settings


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            try:
                timezone.activate(ZoneInfo(tzname))
            except ZoneInfoNotFoundError:
                request.session['django_timezone'] = None
        else:
            try:
                timezone.activate(ZoneInfo(settings.TIME_ZONE_INTERFACE))
            except AttributeError:
                timezone.deactivate()
        return self.get_response(request)
