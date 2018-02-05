from django.contrib import admin
from scheduler.models import Schedule, ExtendedUser, Notification


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("user", "id")
    search_fields = ("user__username", "id")


@admin.register(ExtendedUser)
class ExtendedUserAdmin(admin.ModelAdmin):
    search_fields = ("username", "email")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "msg", "date")
    list_filter = ("read",)
    search_fields = ("user__username", "msg")
