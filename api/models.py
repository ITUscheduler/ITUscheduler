from django.db import models
from django.urls import reverse
from django.utils import timezone


class SemesterManager(models.Manager):
    def get_queryset(self):
        queryset = super(SemesterManager, self).get_queryset()
        current = queryset.get_or_create(name=self.model.SEMESTER_CHOICES[-1][0])[0]
        current.save()
        return queryset

    def current(self):
        return self.get_queryset().get_or_create(name=self.model.SEMESTER_CHOICES[-1][0])[0]


class Semester(models.Model):
    SPRING_17 = "S17"
    FALL_17 = "F17"
    SPRING_18 = "S18"
    SEMESTER_CHOICES = (
        (SPRING_17, "2016-2017 Spring"),
        (FALL_17, "2017-2018 Fall"),
        (SPRING_18, "2017-2018 Spring")
    )
    name = models.CharField(
        unique=True,
        primary_key=True,
        max_length=3,
        choices=SEMESTER_CHOICES,
        default=SPRING_18
    )
    objects = SemesterManager()

    def __str__(self):
        return self.name


class CourseCode(models.Model):
    refreshed = models.DateTimeField(default=timezone.now)
    code = models.CharField(max_length=10, unique=True, primary_key=True)

    class Meta:
        ordering = ['code']
        get_latest_by = "code"

    def __str__(self):
        return str(self.code)

    def get_absolute_url(self):
        return reverse("courses", kwargs={"slug": self.code})


class Prerequisite(models.Model):
    code = models.CharField(max_length=30, null=True, blank=True)
    min_grade = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        get_latest_by = "code"

    def __str__(self):
        return str(self.code)


class MajorRestriction(models.Model):
    major = models.CharField(max_length=100, unique=True, primary_key=True)

    def __str__(self):
        return str(self.major)


class Course(models.Model):
    semester = models.ForeignKey(Semester, default=Semester.SPRING_18, on_delete=models.SET_DEFAULT)
    lecture_count = models.PositiveSmallIntegerField(default=1)
    course_code = models.ForeignKey(CourseCode, on_delete=models.CASCADE)
    crn = models.PositiveIntegerField(unique=True, primary_key=True)
    catalogue = models.URLField(null=True, blank=True)
    code = models.CharField(max_length=40)
    title = models.CharField(max_length=250)
    instructor = models.CharField(max_length=500)
    capacity = models.PositiveSmallIntegerField()
    enrolled = models.PositiveSmallIntegerField(default=0)
    reservation = models.CharField(max_length=60)
    major_restriction = models.ManyToManyField(MajorRestriction)
    prerequisites = models.ManyToManyField(Prerequisite)
    class_restriction = models.CharField(max_length=110)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['code']
        get_latest_by = "code"

    def is_full(self):
        if self.enrolled < self.capacity:
            return False
        else:
            return True

    def __str__(self):
        lectures = '#' + str(self.crn) + " " + str(self.code) + " " + str(self.title) + "\t| "
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
