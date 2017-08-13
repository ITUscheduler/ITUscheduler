from django.contrib.auth.models import AbstractUser
from django.db import models
from api.models import Course


class ExtendedUser(AbstractUser):
    courses = models.ManyToManyField(Course)
    my_schedule = models.ForeignKey("Schedule", blank=True, null=True)


class Schedule(models.Model):
    user = models.ForeignKey(ExtendedUser, null=True)
    courses = models.ManyToManyField(Course)

    def is_available(self, course):
        if course.is_full():
            return False
        for c in self.courses.all():
            if course.day == c.day and c.time[0] <= course.time[0] <= c.time[1] or c.time[0] <= course.time[1] <= c.time[1]:
                return False
            else:
                continue
        return True

    def __str__(self):
        return str(self.user) + " #" + str(self.id)
