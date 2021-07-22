from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import pytz
from .utils import HTTP_STATUS_CODES
from django.conf import settings


class Request(models.Model):
    response = models.SmallIntegerField(choices=HTTP_STATUS_CODES, default=200)
    method = models.CharField(default='GET', max_length=7)
    path = models.CharField(max_length=255)
    time = models.DateTimeField(default=timezone.now, db_index=True)
    timezone = models.CharField(choices=[(tz, tz) for tz in pytz.all_timezones])
    ip = models.GenericIPAddressField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    referer = models.URLField(max_length=255, blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    is_secure = models.BooleanField(default=False)
