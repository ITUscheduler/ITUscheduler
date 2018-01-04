from django.contrib import admin
from api.models import CourseCode, Course, Prerequisite

admin.site.register(Prerequisite)

@admin.register(CourseCode)
class CourseCodeAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass
