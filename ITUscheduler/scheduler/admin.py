from django.contrib import admin
from scheduler.models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass
