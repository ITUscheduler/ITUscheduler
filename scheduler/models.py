from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from api.models import Course


class ExtendedUser(AbstractUser):
    courses = models.ManyToManyField(Course)
    my_schedule = models.ForeignKey("Schedule", blank=True, null=True, on_delete=models.SET_NULL)


class Schedule(models.Model):
    user = models.ForeignKey(ExtendedUser, null=True, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)

    class Meta:
        get_latest_by = 'id'

    def __str__(self):
        return str(self.user) + " #" + str(self.id)

    def get_absolute_url(self):
        return reverse("schedule", kwargs={"pk": self.id})



class Notification(models.Model):
    user = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    msg = models.CharField(max_length=1000)
    read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.msg)
