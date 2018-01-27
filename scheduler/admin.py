from django.contrib import admin
from scheduler.models import Schedule, ExtendedUser, Notification


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass


@admin.register(ExtendedUser)
class ExtendedUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Notification)
class NotificationUserAdmin(admin.ModelAdmin):
    pass
