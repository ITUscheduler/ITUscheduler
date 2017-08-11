from django.contrib.auth.models import AbstractUser
from django.db import models
from api.models import Course


class Schedule(models.Model):
    courses = models.ManyToManyField(Course)

    def is_available(self, course):
        if course.is_full():
            return False
        for c in self.courses_set.all():
            if course.day == c.day and c.time[0] <= course.time[0] <= c.time[1] or c.time[0] <= course.time[1] <= c.time[1]:
                return False
            else:
                continue
        return True


class ExtendedUser(AbstractUser):
    courses = models.ManyToManyField(Course)
    my_schedule = models.ForeignKey(Schedule, related_name="my_schedule", blank=True, null=True)
    schedules = models.ManyToManyField(Schedule, related_name="schedules")
