from django.db import models


class CourseCode(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.code


class Course(models.Model):
    course_code = models.ForeignKey(CourseCode)
    crn = models.PositiveIntegerField()
    code = models.CharField(max_length=3)
    title = models.CharField(max_length=100)
    instructor = models.CharField(max_length=200)
    building = models.CharField(max_length=3)
    day = models.CharField(max_length=20)
    time_start = models.PositiveIntegerField()
    time_finish = models.PositiveIntegerField()
    room = models.CharField(max_length=20)
    capacity = models.PositiveSmallIntegerField()
    enrolled = models.PositiveSmallIntegerField(default=0)
    reservation = models.CharField(max_length=50)
    major_restriction = models.TextField()
    prerequisites = models.TextField()
    class_restriction = models.CharField(max_length=20)

    class Meta:
        get_latest_by = "crn"

    def __str__(self):
        return str(self.crn) + " " + self.course_code.code + " " + self.title

    def is_full(self):
        if self.enrolled < self.capacity:
            return False
        else:
            return True
