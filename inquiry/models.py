from django.db import models
from django.utils import timezone
import pytz
from ipware import get_client_ip
from .utils import HTTP_STATUS_CODES
from django.conf import settings


class Request(models.Model):
    response = models.SmallIntegerField(choices=HTTP_STATUS_CODES, default=200)
    method = models.CharField(default='GET', max_length=7)
    path = models.CharField(max_length=255)
    time = models.DateTimeField(default=timezone.now, db_index=True)
    timezone = models.CharField(max_length=100, choices=[(tz, tz) for tz in pytz.all_timezones])
    ip = models.GenericIPAddressField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    referer = models.URLField(max_length=255, blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    is_secure = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.time} {self.method} {self.path} {self.response}"

    def create_from_request(self, request, response):
        self.method = request.method
        self.path = request.path
        self.is_secure = request.is_secure()

        self.ip, _ = get_client_ip(request) if not None else '0.0.0.0'
        self.referer = request.META.get('HTTP_REFERER', '')[:255]
        self.user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
        self.language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')[:255]
        if request.user:
            if request.user.is_authenticated:
                self.user = request.user
        self.save()
