from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from api.models import Course, MajorCode, Semester


def get_semester():
    try:
        semester = Semester.objects.current()
        return semester.pk
    except Exception:
        return 0


class ExtendedUser(AbstractUser):
    courses = models.ManyToManyField(Course, blank=True)
    my_major_code = models.ForeignKey(MajorCode, blank=True, null=True, on_delete=models.SET_NULL)
    my_semester = models.ForeignKey(Semester, default=get_semester(), on_delete=models.SET_DEFAULT)
    my_schedule = models.ForeignKey("Schedule", blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.username)


class Schedule(models.Model):
    user = models.ForeignKey(ExtendedUser, null=True, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)

    class Meta:
        get_latest_by = 'id'

    def __str__(self):
        if self.user:
            for index, schedule in enumerate(self.user.schedule_set.all()):
                if schedule.id == self.id:
                    return str(self.user) + " #" + str(index + 1)
        else:
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
