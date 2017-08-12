import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from django.core import serializers
from api.models import CourseCode, Course

BASE_URL = "http://www.sis.itu.edu.tr/tr/ders_programlari/LSprogramlar/prg.php?fb="


@user_passes_test(lambda u: u.is_superuser)
def db_refresh(request):
    CourseCode.objects.all().delete()
    Course.objects.all().delete()

    r = requests.get(BASE_URL)
    soup = BeautifulSoup(r.content, "html.parser")

    for option in soup.find("select").find_all("option"):
        if option.attrs["value"] != "":
            CourseCode.objects.create(code=option.get_text()[:-1:])

    for course_code in CourseCode.objects.all():
        r = requests.get(BASE_URL + course_code.code)
        soup = BeautifulSoup(r.content, "html.parser")

        i = 5
        while True:
            try:
                raw_course = soup.select_one("tr:nth-of-type({})".format(i))
                try:
                    data = [row.get_text() for row in raw_course.find_all("td")]
                    n = len(data[4]) // 3
                    for index in range(n):
                        time = data[6][:-1:].split()[index].split("/")
                        if "" in time:
                            time = ["2500", "2500"]
                        if time[index][0] == "0":
                            time[index] = time[index][1::]
                        prerequisites = str(data[12])
                        prerequisites.replace("veya", " veya")
                        Course.objects.create(
                            course_code=course_code,
                            crn=int(data[0]),
                            code=data[1],
                            title=data[2],
                            instructor=data[3],
                            building=data[4][3*index:3*index+3:],
                            day=data[5].split()[index],
                            time_start=int(time[0]),
                            time_finish=int(time[1]),
                            room=data[7].split()[index],
                            capacity=int(data[8]),
                            enrolled=int(data[9]),
                            reservation=data[10],
                            major_restriction=data[11],
                            prerequisites=prerequisites,
                            class_restriction=data[13]
                        )
                    i += 1
                except AttributeError as error:
                    i += 1
            except IndexError as error:
                break

    return HttpResponse("<a href='/'><h1>Course Codes and Courses refreshed!</h1></a>")


@user_passes_test(lambda u: u.is_superuser)
def db_flush(request):
    CourseCode.objects.all().delete()
    Course.objects.all().delete()

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


def get_courses(request):
    course_codes = CourseCode.objects.all()

    if len(course_codes) == 0:
        return HttpResponseNotFound(content="<a href='/'><h1>First refresh database to get Course Codes!</h1></a>")

    courses = []
    for course_code in course_codes:
        r = requests.get(BASE_URL + course_code.code)
        soup = BeautifulSoup(r.content, "html.parser")

        i = 5
        while True:
            try:
                raw_course = soup.select_one("tr:nth-of-type({})".format(i))
                try:
                    data = [row.get_text() for row in raw_course.find_all("td")]
                    n = len(data[4]) // 3
                    for index in range(n):
                        time = data[6][:-1:].split()[index].split("/")
                        if "" in time:
                            time = ["2500", "2500"]
                        if time[index][0] == "0":
                            time[index] = time[index][1::]
                        prerequisites = str(data[12])
                        prerequisites.replace("veya", " veya")
                        courses.append(Course(
                            course_code=course_code,
                            crn=int(data[0]),
                            code=data[1],
                            title=data[2],
                            instructor=data[3],
                            building=data[4][3*index:3*index+3:],
                            day=data[5].split()[index],
                            time_start=int(time[0]),
                            time_finish=int(time[1]),
                            room=data[7].split()[index],
                            capacity=int(data[8]),
                            enrolled=int(data[9]),
                            reservation=data[10],
                            major_restriction=data[11],
                            prerequisites=prerequisites,
                            class_restriction=data[13]
                        ))
                    i += 1
                except AttributeError as error:
                    i += 1
            except IndexError as error:
                break

    params = {"sort_keys": True, "indent": 4}
    return JsonResponse({"courses": serializers.serialize("json", courses)}, json_dumps_params=params)
