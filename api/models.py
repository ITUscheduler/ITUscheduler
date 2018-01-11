from django.db import models
from django.utils import timezone


class CourseCode(models.Model):
    refreshed = models.DateTimeField(default=timezone.now)
    code = models.CharField(max_length=10, unique=True, primary_key=True)

    def __str__(self):
        return str(self.code)


class Prerequisite(models.Model):
    code = models.CharField(max_length=30, null=True, blank=True)
    min_grade = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.code)


class MajorRestriction(models.Model):
    major = models.CharField(max_length=100, unique=True, primary_key=True)

    def __str__(self):
        return str(self.major)


class Course(models.Model):
    lecture_count = models.PositiveSmallIntegerField(default=1)
    course_code = models.ForeignKey(CourseCode, on_delete=models.CASCADE)
    crn = models.PositiveIntegerField(unique=True, primary_key=True)
    code = models.CharField(max_length=40)
    title = models.CharField(max_length=250)
    instructor = models.CharField(max_length=200)
    capacity = models.PositiveSmallIntegerField()
    enrolled = models.PositiveSmallIntegerField(default=0)
    reservation = models.CharField(max_length=60)
    major_restriction = models.ManyToManyField(MajorRestriction)
    prerequisites = models.ManyToManyField(Prerequisite)
    class_restriction = models.CharField(max_length=110)

    class Meta:
        get_latest_by = "crn"

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


class Lecture(models.Model):
    building = models.CharField(max_length=65)
    day = models.CharField(max_length=60)
    time_start = models.IntegerField()
    time_finish = models.IntegerField()
    room = models.CharField(max_length=55)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.course)

    def time_str_tuple(self):
        time_start = str(self.time_start)[:-2] + ":" + str(self.time_start)[-2:]
        time_finish = str(self.time_finish)[:-2] + ":" + str(self.time_finish)[-2:]
        return time_start, time_finish
