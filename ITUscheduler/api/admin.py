from django.contrib import admin
from api.models import CourseCode, Course


@admin.register(CourseCode)
class CourseCodeAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass
