from django.contrib import admin
from scheduler.models import Schedule, ExtendedUser


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass


@admin.register(ExtendedUser)
class ExtendedUserAdmin(admin.ModelAdmin):
    pass
