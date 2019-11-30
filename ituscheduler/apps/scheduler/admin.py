from django.contrib import admin

from .models import (
    Schedule,
    ExtendedUser,
    Notification,
)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("user", "id")
    search_fields = ("user__username", "id")
    raw_id_fields = ("courses",)


@admin.register(ExtendedUser)
class ExtendedUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "my_schedule", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name", "my_schedule__id")
    raw_id_fields = ("courses",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "msg", "date")
    list_filter = ("read",)
    search_fields = ("user__username", "msg")
