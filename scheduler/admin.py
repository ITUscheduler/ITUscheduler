from django.contrib import admin
from scheduler.models import Schedule, ExtendedUser, Notification


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    search_fields = ("user__username", "user__email")


@admin.register(ExtendedUser)
class ExtendedUserAdmin(admin.ModelAdmin):
    search_fields = ("username", "email")


@admin.register(Notification)
class NotificationUserAdmin(admin.ModelAdmin):
    list_filter = ("read",)
    search_fields = ("user__username",)
