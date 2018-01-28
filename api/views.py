import requests
import re
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from api.models import CourseCode, Course, Lecture, Prerequisite, MajorRestriction
from scheduler.models import Schedule, Notification
from django.utils import timezone
from django.core.mail import send_mail

BASE_URL = "http://www.sis.itu.edu.tr/tr/ders_programlari/LSprogramlar/prg.php?fb="


def notify_course_removal(course):
    schedules = course.schedule_set.all()
    users = list(set([schedule.user for schedule in schedules]))

    for user in users:
        notification = Notification()
        notification.user = user
        notification.msg = 'Course #{} in your schedule #{} has been removed from ITU SIS. Please update your schedule according to the new changes.\n\nITUscheduler loves you.'.format(course.crn, ", #".join([str(schedule.id) for schedule in schedules]))
        notification.save()
        recipients = [user.email, 'info@ituscheduler.com', 'dorukgezici96@gmail.com', 'altunerism@gmail.com']
        send_mail(
            '[ITUscheduler] | Course #{} is Removed'.format(course.crn),
            '\tCourse #{} in your schedule #{} has been removed from ITU SIS. Please update your schedule according to the new changes.\n\nITUscheduler loves you.'.format(
                course.crn, ", #".join([str(schedule.id) for schedule in schedules])),
            'info@ituscheduler.com',
            recipients,
        )


class RefreshCoursesView(UserPassesTestMixin, generic.ListView):
    model = CourseCode
    template_name = "refresh_courses.html"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False


@user_passes_test(lambda u: u.is_superuser)
def db_refresh_course_codes(request):
    r = requests.get(BASE_URL)
    soup = BeautifulSoup(r.content, "html.parser")
    codes = [course_code.code for course_code in CourseCode.objects.all()]

    for option in soup.find("select").find_all("option"):
        if option.attrs["value"] != "":
            opt = option.get_text()[:-1:]
            if opt in codes:
                codes.remove(opt)
            query = CourseCode.objects.filter(code=opt)
            if not query.exists():
                CourseCode.objects.create(code=opt)
    for code in codes:
        course_code = CourseCode.objects.get(code=code)
        course_code.delete()
    return HttpResponse("<a href='/'><h1>Course Codes refreshed!</h1></a>")


@user_passes_test(lambda u: u.is_superuser)
def db_refresh_courses(request):
    codes = request.POST.getlist("course_codes[]")
    with transaction.atomic():
        for code in codes:
            course_code = get_object_or_404(CourseCode, code=code)
            crns = [course.crn for course in Course.unfiltered.filter(course_code=code)]
            active_crns = [course.crn for course in Course.objects.filter(course_code=code)]

            r = requests.get(BASE_URL + code)
            soup = BeautifulSoup(r.content, "html5lib")
            raw_table = soup.find("table", class_="dersprg")

            nth_course = 3
            new_crns = []
            while True:
                try:
                    raw_course = raw_table.select_one("tr:nth-of-type({})".format(nth_course))
                    if raw_course is None:
                        break
                    try:
                        data = [row.get_text() for row in raw_course.find_all("td")]
                        rows = raw_course.find_all("td")
                        lecture_count = len(data[4]) // 3
                        crn = int(data[0])
                        new_crns.append(crn)
                        times_start = ""
                        times_finish = ""
                        for index in range(lecture_count):

                            time = data[6][:-1:].split()[index].split("/")

                            if "" in time or "----" in time:
                                time = ["2500", "2500"]
                            for i in range(2):
                                if time[i][0] == "0":
                                    time[i] = time[i][1::]

                            times_start += time[0] + ","
                            times_finish += time[1] + ","

                        times_start = times_start[:-1:]
                        times_finish = times_finish[:-1:]

                        prerequisites = re.sub("veya", " veya", data[12])

                        buildings = [data[4][3 * i:3 * i + 3:] for i in range(lecture_count)]
                        days = data[5].split()
                        majors = data[11].split(", ")
                        prerequisites_objects = []
                        if 'Yok/None' not in prerequisites and 'Diğer Şartlar' not in prerequisites and "Özel":
                            for prerequisite in prerequisites.split(' veya '):
                                prerequisite = prerequisite.split(' ')
                                course = " ".join(prerequisite[:2])
                                grade = str(prerequisite[-1])

                                try:
                                    prerequisites_objects.append(Prerequisite.objects.get(code=course,
                                                                                          min_grade=grade))
                                except Prerequisite.DoesNotExist:
                                    prerequisites_objects.append(
                                        Prerequisite.objects.create(code=course, min_grade=grade))
                        else:
                            prerequisites_objects.append(Prerequisite.objects.get_or_create(code=None)[0])

                        if crn in crns:
                            course = Course.unfiltered.get(crn=crn)
                            course.lecture_count = lecture_count
                            course.course_code = course_code
                            course.code = data[1]
                            course.catalogue = rows[1].contents[0]["href"]
                            course.title = data[2]
                            course.instructor = data[3]
                            course.capacity = int(data[8])
                            course.enrolled = int(data[9])
                            course.reservation = data[10]
                            course.class_restriction = data[13]
                            course.active = True

                            course.save()

                            for lecture in course.lecture_set.all():
                                lecture.delete()
                        else:
                            course = Course.unfiltered.create(
                                lecture_count=lecture_count,
                                course_code=course_code,
                                crn=crn,
                                catalogue=rows[1].contents[0]["href"],
                                code=data[1],
                                title=data[2],
                                instructor=data[3],
                                capacity=int(data[8]),
                                enrolled=int(data[9]),
                                reservation=data[10],
                                class_restriction=data[13]
                            )

                        for i in range(lecture_count):
                            time_start = times_start.split(",")[i]
                            time_finish = times_finish.split(",")[i]

                            Lecture.objects.create(
                                building=buildings[i],
                                day=days[i],
                                time_start=time_start,
                                time_finish=time_finish,
                                room=data[7].split()[i],
                                course=course
                            )

                        for major in majors:
                            major_restriction, _ = MajorRestriction.objects.get_or_create(major=major)
                            course.major_restriction.add(major_restriction)

                        for prerequisite in prerequisites_objects:
                            course.prerequisites.add(prerequisite)

                        nth_course += 1
                    except AttributeError:
                        nth_course += 1
                except IndexError:
                    break

            removed_crns = [crn for crn in active_crns if crn not in new_crns]
            for removed_crn in removed_crns:
                old_course = Course.objects.get(crn=removed_crn)
                notify_course_removal(old_course)
                old_course.active = False
                old_course.save()
                print("Course {} is removed from ITU SIS.".format(old_course))

            course_code.refreshed = timezone.now()
            course_code.save()
    return HttpResponse("<a href='/api/refresh/courses'><h1>{} Courses refreshed!</h1></a>".format(", ".join(codes)))


@user_passes_test(lambda u: u.is_superuser)
def db_flush(request):
    CourseCode.objects.all().delete()
    Course.objects.all().delete()
    Schedule.objects.all().delete()

    return HttpResponse("<a href='/'><h1>Course Codes and Courses flushed!</h1></a>")
