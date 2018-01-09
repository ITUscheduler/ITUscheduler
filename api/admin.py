from django.contrib import admin
from api.models import CourseCode, Course, Prerequisite, MajorRestriction, Lecture


@admin.register(CourseCode)
class CourseCodeAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


admin.site.register(Prerequisite)
admin.site.register(MajorRestriction)
admin.site.register(Lecture)
