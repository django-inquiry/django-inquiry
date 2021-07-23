from django.contrib import admin
from django.urls import path
from .views import ChartView

from .models import Request

class RequestAdmin(admin.ModelAdmin):
    list_display = ('time', 'path', 'response', 'method')

    def get_urls(self):
        urls = super(RequestAdmin, self).get_urls()
        custom_urls = [
            path('charts/', self.admin_site.admin_view(ChartView.as_view()), name='charts')
        ]
        return custom_urls + urls

admin.site.register(Request, RequestAdmin)
