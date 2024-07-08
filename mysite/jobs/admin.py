# jobs/admin.py
from django.contrib import admin
from .models import Job

class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'queue', 'available_at', 'reserved_at', 'attempts')
    list_filter = ('queue', 'available_at', 'reserved_at')
    search_fields = ('queue', 'payload')

admin.site.register(Job, JobAdmin)
