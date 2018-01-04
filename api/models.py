from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.utils import timezone


class CourseCode(models.Model):
    refreshed = models.DateTimeField(default=timezone.now)
    code = models.CharField(max_length=3, unique=True, primary_key=True)

    def __str__(self):
        return self.code


class Course(models.Model):
    n_lectures = models.PositiveSmallIntegerField(default=1)
    course_code = models.ForeignKey(CourseCode, on_delete=models.CASCADE)
    crn = models.PositiveIntegerField(unique=True, primary_key=True)
    code = models.CharField(max_length=3)
    title = models.CharField(max_length=100)
    instructor = models.CharField(max_length=200)
    # building = models.CharField(max_length=20)
    # day = models.CharField(max_length=50)
    # time_start = models.CharField(max_length=40, validators=[validate_comma_separated_integer_list])
    # time_finish = models.CharField(max_length=40, validators=[validate_comma_separated_integer_list])
    # room = models.CharField(max_length=50)
    capacity = models.PositiveSmallIntegerField()
    enrolled = models.PositiveSmallIntegerField(default=0)
    reservation = models.CharField(max_length=50)
    major_restriction = models.TextField()
    prerequisites = models.TextField()
    class_restriction = models.CharField(max_length=20)

    class Meta:
        get_latest_by = "crn"

    def __str__(self):
        string = "#" + str(self.crn) + " " + self.code + " " + self.title + " / " + self.instructor + " | " + " ".join([lecture.building for lecture in self.lecture_set.all()]) + " " + " ".join([lecture.day for lecture in self.lecture_set.all()]) + " "
        for i in range(self.n_lectures):
            string += "{}/{}".format(self.lecture_set.all()[i].time_start, self.lecture_set.all()[i].time_finish)
            if i + 1 != self.n_lectures:
                string += ","
        string += " | " + "{}/{}".format(self.enrolled, self.capacity)
        return string

    def is_full(self):
        if self.enrolled < self.capacity:
            return False
        else:
            return True


class Lecture(models.Model):
    building = models.CharField(max_length=20)
    day = models.CharField(max_length=50)
    time_start = models.IntegerField()
    time_finish = models.IntegerField()
    room = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
