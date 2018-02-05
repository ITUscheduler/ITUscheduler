from django.contrib import admin
from api.models import CourseCode, Course, Prerequisite, MajorRestriction, Lecture, Semester


@admin.register(CourseCode)
class CourseCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "refreshed")
    search_fields = ("code",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_filter = ("active", "semester__name")
    list_display = ("crn", "course_code", "code", "title", "instructor", "lecture_count", "enrolled", "capacity", "reservation", "class_restriction", "catalogue", "active")
    search_fields = ("course_code__code", "crn")


@admin.register(Prerequisite)
class PrerequisiteAdmin(admin.ModelAdmin):
    list_display = ("code", "min_grade")
    search_fields = ("code",)


@admin.register(MajorRestriction)
class MajorRestrictionAdmin(admin.ModelAdmin):
    list_display = ("major",)
    search_fields = ("major",)


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ("course", "building", "room", "day", "time_start", "time_finish")
    search_fields = ("course__crn", "building", "room", "day", "time_start", "time_finish")


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("__str__", "name",)
