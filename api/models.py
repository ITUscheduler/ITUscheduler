from django.core.validators import validate_comma_separated_integer_list
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
        string = "#" + str(self.crn) + " " + self.code + " " + self.title + " / " + self.instructor + " | " + " ".join([lecture.building for lecture in self.lecture_set.all()]) + " " + " ".join([lecture.day for lecture in self.lecture_set.all()]) + " "
        for i in range(self.lecture_count):
            string += "{}/{}".format(self.lecture_set.all()[i].time_start, self.lecture_set.all()[i].time_finish)
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
        data = {
            'buildings': [],
            'days': [],
            'rooms': [],
            'times_start': [],
            'times_finish': [],
        }

        for lecture in self.lecture_set.all():
            data['buildings'].append(lecture.building)
            data['days'].append(lecture.days)
            data['rooms'].append(lecture.rooms)
            data['times_start'].append(lecture.times_start)
            data['times_finish'].append(lecture.time_finish)

        data['buildings'] = ' '.join(data['buildings'])
        data['days'] = ' '.join(data['daysrooms'])
        data['rooms'] = ' '.join(data['rooms'])
        data['times_start'] = ' '.join(data['times_start'])
        data['times_finish'] = ' '.join(data['times_finish'])

        return data


class Lecture(models.Model):
    building = models.CharField(max_length=20)
    day = models.CharField(max_length=50)
    time_start = models.IntegerField()
    time_finish = models.IntegerField()
    room = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.course)
