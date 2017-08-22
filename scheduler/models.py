from django.contrib.auth.models import AbstractUser
from django.db import models
from api.models import Course


class ExtendedUser(AbstractUser):
    courses = models.ManyToManyField(Course)
    my_schedule = models.ForeignKey("Schedule", blank=True, null=True, on_delete=models.SET_NULL)


class Schedule(models.Model):
    user = models.ForeignKey(ExtendedUser, null=True)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return str(self.user) + " #" + str(self.id)
