import requests
import re
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.views import generic
from api.models import CourseCode, Course, Lecture
from scheduler.models import Schedule
from django.utils import timezone

BASE_URL = "http://www.sis.itu.edu.tr/tr/ders_programlari/LSprogramlar/prg.php?fb="


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
            crns = [course.crn for course in Course.objects.filter(course_code=code).all()]

            r = requests.get(BASE_URL + code)
            soup = BeautifulSoup(r.content, "html5lib")
            raw_table = soup.find("table", class_="dersprg")

            nth_course = 3
            while True:
                try:
                    raw_course = raw_table.select_one("tr:nth-of-type({})".format(nth_course))
                    if raw_course is None:
                        break
                    try:
                        data = [row.get_text() for row in raw_course.find_all("td")]
                        lecture_count = len(data[4]) // 3
                        crn = int(data[0])
                        times_start = ""
                        times_finish = ""
                        for index in range(lecture_count):
                            time = data[6][:-1:].split()[index].split("/")
                            if "" in time:
                                time = ["2500", "2500"]
                            for i in range(2):
                                if time[i][0] == "0":
                                    time[i] = time[i][1::]
                            times_start += time[0] + ","
                            times_finish += time[1] + ","
                        times_start = times_start[:-1:]
                        times_finish = times_finish[:-1:]
                        prerequisites = data[12]
                        prerequisites = re.sub("veya", " veya", prerequisites)
                        if crn in crns:
                            _ = Course.objects.get(crn=crn)
                            # Edit course object (Not implemented)
                        else:
                            buildings = [data[4][3*i:3*i+3:] for i in range(lecture_count)]
                            days = data[5].split()

                            course = Course.objects.create(
                                lecture_count=lecture_count,
                                course_code=course_code,
                                crn=crn,
                                code=data[1],
                                title=data[2],
                                instructor=data[3],
                                capacity=int(data[8]),
                                enrolled=int(data[9]),
                                reservation=data[10],
                                major_restriction=data[11],
                                prerequisites=prerequisites,
                                class_restriction=data[13]
                            )

                            for i in range(lecture_count):
                                Lecture.objects.create(
                                    building=buildings[i],
                                    day=days[i],
                                    time_start=times_start.split(",")[i],
                                    time_finish=times_finish.split(",")[i],
                                    room=data[7].split()[i],
                                    course=course
                                )

                        nth_course += 1
                    except AttributeError:
                        nth_course += 1
                except IndexError:
                    break

            course_code.refreshed = timezone.now()
            course_code.save()
    return HttpResponse("<a href='/'><h1>{} Courses refreshed!</h1></a>".format(", ".join(codes)))


@user_passes_test(lambda u: u.is_superuser)
def db_flush(request):
    CourseCode.objects.all().delete()
    Course.objects.all().delete()
    Schedule.objects.all().delete()

    return HttpResponse("<a href='/'><h1>Course Codes and Courses flushed!</h1></a>")


def get_course_codes(request):
    r = requests.get(BASE_URL)
    soup = BeautifulSoup(r.content, "html.parser")

    course_codes = []
    for option in soup.find("select").find_all("option"):
        if option.attrs["value"] != "":
            course_codes.append(CourseCode(code=option.get_text()[:-1:]))

    params = {"sort_keys": True, "indent": 4}
    return JsonResponse({"course_codes": [course_code.code for course_code in course_codes]}, json_dumps_params=params)


# def get_courses(request):
#     course_codes = CourseCode.objects.all()
#
#     if len(course_codes) == 0:
#         return HttpResponseNotFound(content="<a href='/'><h1>First refresh database to get Course Codes!</h1></a>")
#
#     courses = []
#     for course_code in course_codes:
#         r = requests.get(BASE_URL + course_code.code)
#         soup = BeautifulSoup(r.content, "html.parser")
#
#         i = 5
#         while True:
#             try:
#                 raw_course = soup.select_one("tr:nth-of-type({})".format(i))
#                 try:
#                     data = [row.get_text() for row in raw_course.find_all("td")]
#                     n = len(data[4]) // 3
#                     for index in range(n):
#                         time = data[6][:-1:].split()[index].split("/")
#                         if "" in time:
#                             time = ["2500", "2500"]
#                         if time[index][0] == "0":
#                             time[index] = time[index][1::]
#                         prerequisites = str(data[12])
#                         prerequisites.replace("veya", " veya")
#                         courses.append(Course(
#                             course_code=course_code,
#                             crn=int(data[0]),
#                             code=data[1],
#                             title=data[2],
#                             instructor=data[3],
#                             building=data[4][3*index:3*index+3:],
#                             day=data[5].split()[index],
#                             time_start=int(time[0]),
#                             time_finish=int(time[1]),
#                             room=data[7].split()[index],
#                             capacity=int(data[8]),
#                             enrolled=int(data[9]),
#                             reservation=data[10],
#                             major_restriction=data[11],
#                             prerequisites=prerequisites,
#                             class_restriction=data[13]
#                         ))
#                     i += 1
#                 except AttributeError:
#                     i += 1
#             except IndexError:
#                 break
#
#     params = {"sort_keys": True, "indent": 4}
#     return JsonResponse({"courses": serializers.serialize("json", courses)}, json_dumps_params=params)
