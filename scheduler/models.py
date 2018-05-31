from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from api.models import Course, MajorCode, Semester


class ExtendedUser(AbstractUser):
    courses = models.ManyToManyField(Course)
    my_major_code = models.ForeignKey(MajorCode, default="BLG", blank=True, null=True, on_delete=models.SET_DEFAULT)
    my_semester = models.ForeignKey(Semester, default=Semester.objects.current().pk, on_delete=models.SET_DEFAULT)
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
    msg = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.msg)
