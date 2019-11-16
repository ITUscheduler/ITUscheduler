from django.db import models
from django.urls import reverse
from django.utils import timezone
import uuid


class SemesterManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        current = qs.get_or_create(name=self.model.CURRENT_SEMESTER)[0]
        current.save()
        return qs

    def current(self):
        return self.get_queryset().get_or_create(name=self.model.CURRENT_SEMESTER)[0]


class Semester(models.Model):
    SUMMER_20 = "SU20"
    SPRING_20 = "S20"
    FALL_19 = "F19"
    SUMMER_19 = "SU19"
    SPRING_19 = "S19"
    FALL_18 = "F18"
    SUMMER_18 = "SU18"
    SPRING_18 = "S18"
    FALL_17 = "F17"
    SPRING_17 = "S17"
    CURRENT_SEMESTER = FALL_19
    SEMESTER_CHOICES = (
        (SUMMER_20, "2019-2020 Summer"),
        (SPRING_20, "2019-2020 Spring"),
        (FALL_19, "2019-2020 Fall"),
        (SUMMER_19, "2018-2019 Summer"),
        (SPRING_19, "2018-2019 Spring"),
        (FALL_18, "2018-2019 Fall"),
        (SUMMER_18, "2017-2018 Summer"),
        (SPRING_18, "2017-2018 Spring"),
        (FALL_17, "2017-2018 Fall"),
        (SPRING_17, "2016-2017 Spring")
    )
    SEMESTER_CHOICES_TURKISH = (
        (SUMMER_20, "2019-2020 Yaz"),
        (SPRING_20, "2019-2020 Bahar"),
        (FALL_19, "2019-2020 Güz"),
        (SUMMER_19, "2018-2019 Yaz"),
        (SPRING_19, "2018-2019 Bahar"),
        (FALL_18, "2018-2019 Güz"),
        (SUMMER_18, "2017-2018 Yaz"),
        (SPRING_18, "2017-2018 Bahar"),
        (FALL_17, "2017-2018 Güz"),
        (SPRING_17, "2016-2017 Bahar")
    )
    name = models.CharField(
        unique=True,
        primary_key=True,
        max_length=4,
        choices=SEMESTER_CHOICES,
        default=CURRENT_SEMESTER
    )
    objects = SemesterManager()

    def __str__(self):
        return str(self.name)


class MajorCode(models.Model):
    refreshed = models.DateTimeField(default=timezone.now)
    code = models.CharField(max_length=10, unique=True, primary_key=True)

    class Meta:
        ordering = ['code']
        get_latest_by = "code"

    def get_absolute_url(self):
        return reverse("courses") + "?major={}".format(self.code)

    def __str__(self):
        return str(self.code)


class Prerequisite(models.Model):
    code = models.CharField(max_length=30, null=True, blank=True)
    min_grade = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        get_latest_by = "code"

    def __str__(self):
        return str(self.code) + " (MIN " + str(self.min_grade) + ")"


class MajorRestriction(models.Model):
    major = models.CharField(max_length=100, unique=True, primary_key=True)

    def __str__(self):
        return str(self.major)


class CourseManager(models.Manager):
    def inactive(self):
        return super().get_queryset().filter(active=False)

    def active(self):
        return super().get_queryset().filter(active=True)


class Course(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    semester = models.ForeignKey(Semester, default=Semester.CURRENT_SEMESTER, on_delete=models.CASCADE)
    lecture_count = models.PositiveSmallIntegerField(default=1)
    major_code = models.ForeignKey(MajorCode, on_delete=models.CASCADE)
    crn = models.PositiveIntegerField(unique=True, primary_key=True)
    catalogue = models.URLField(null=True, blank=True)
    code = models.CharField(max_length=40)
    title = models.CharField(max_length=250)
    instructor = models.CharField(max_length=500)
    capacity = models.PositiveSmallIntegerField()
    enrolled = models.PositiveSmallIntegerField(default=0)
    reservation = models.CharField(max_length=100)
    major_restriction = models.ManyToManyField(MajorRestriction)
    prerequisites = models.ManyToManyField(Prerequisite)
    class_restriction = models.CharField(max_length=110)
    active = models.BooleanField(default=True)
    objects = CourseManager()

    class Meta:
        unique_together = (("semester", "crn"),)
        ordering = ['code']
        get_latest_by = "code"

    def is_full(self):
        if self.enrolled < self.capacity:
            return False
        else:
            return True

    def __str__(self):
        lectures = "{} #{} {} {} | {} | ".format(self.semester.get_name_display(), self.crn, self.code, self.title, self.instructor)
        for lecture in self.lecture_set.all():
            lectures += "{} {} {} {} | ".format(lecture.building, lecture.day, *lecture.time_str_tuple())
        lectures += str(self.enrolled) + "/" + str(self.capacity) + " Capacity"
        return lectures

    def get_code_only(self):
        return self.code.split(' ')[-1]


class Lecture(models.Model):
    building = models.CharField(max_length=65)
    day = models.CharField(max_length=60)
    time_start = models.IntegerField()
    time_finish = models.IntegerField()
    room = models.CharField(max_length=55)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        ordering = ['course']
        get_latest_by = "course"

    def __str__(self):
        return str(self.course)

    def time_str_tuple(self):
        time_start = str(self.time_start)[:-2] + ":" + str(self.time_start)[-2:]
        time_finish = str(self.time_finish)[:-2] + ":" + str(self.time_finish)[-2:]
        return time_start, time_finish
