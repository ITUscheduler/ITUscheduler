from django.db import models
from django.utils import timezone


class CourseCode(models.Model):
    refreshed = models.DateTimeField(default=timezone.now)
    code = models.CharField(max_length=3, unique=True, primary_key=True)

    def __str__(self):
        return self.code


class Course(models.Model):
    lecture_count = models.PositiveSmallIntegerField(default=1)
    course_code = models.ForeignKey(CourseCode, on_delete=models.CASCADE)
    crn = models.PositiveIntegerField(unique=True, primary_key=True)
    code = models.CharField(max_length=3)
    title = models.CharField(max_length=100)
    instructor = models.CharField(max_length=200)
    capacity = models.PositiveSmallIntegerField()
    enrolled = models.PositiveSmallIntegerField(default=0)
    reservation = models.CharField(max_length=50)
    major_restriction = models.TextField()
    prerequisites = models.TextField()
    class_restriction = models.CharField(max_length=20)

    class Meta:
        get_latest_by = "crn"

    def __str__(self):
        lecture_attrs = self.get_lecture_attrs()
        string = "#" + str(self.crn) + " " + self.code + " " + self.title + " / " + self.instructor + " | " + lecture_attrs["buildings"] + " " + lecture_attrs["days"] + " "
        for i in range(self.lecture_count):
            string += "{}/{}".format(lecture_attrs["times_start"][i], lecture_attrs["times_finish"][i])
            if i + 1 != self.lecture_count:
                string += ","
        string += " | " + "{}/{}".format(self.enrolled, self.capacity)
        return string

    def is_full(self):
        if self.enrolled < self.capacity:
            return False
        else:
            return True

    def get_lecture_attrs(self):
        attrs = {
            'buildings': '',
            'days': '',
            'rooms': '',
            'times_start': '',
            'times_finish': '',
        }
        buildings, days, rooms = [], [], []
        times_start, times_finish = [], []
        for lecture in self.lecture_set.all():
            buildings.append(str(lecture.building))
            days.append(str(lecture.day))
            rooms.append(str(lecture.room))
            times_start.append(str(lecture.time_start))
            times_finish.append(str(lecture.time_finish))
        attrs['buildings'] = ' '.join(buildings)
        attrs['days'] = ' '.join(days)
        attrs['rooms'] = ' '.join(rooms)
        attrs['times_start'] = ' '.join(times_start)
        attrs['times_finish'] = ' '.join(times_finish)
        return attrs


class Lecture(models.Model):
    building = models.CharField(max_length=20)
    day = models.CharField(max_length=50)
    time_start = models.IntegerField()
    time_finish = models.IntegerField()
    room = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.course)
