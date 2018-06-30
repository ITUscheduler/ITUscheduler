import re
from django.utils import timezone
import requests
from bs4 import BeautifulSoup
from celery import shared_task
from django.shortcuts import get_object_or_404
from api.models import Semester, MajorCode, Course, Prerequisite, MajorRestriction, Lecture
from api.views import BASE_URL


@shared_task(bind=True)
def refresh_courses(self):
    codes = [code.code for code in MajorCode.objects.all()]

    for code in codes:
        major_code = get_object_or_404(MajorCode, code=code)

        r = requests.get(BASE_URL + code)
        soup = BeautifulSoup(r.content, "html5lib")
        semester = Semester.objects.current()
        crns = [course.crn for course in Course.objects.filter(major_code=code, semester=semester)]
        active_crns = [course.crn for course in Course.objects.active().filter(major_code=code, semester=semester)]

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

                    buildings_raw = rows[4].contents[0].contents
                    buildings = []
                    length = len(buildings_raw) // 2
                    for i in range(length):
                        buildings.append(buildings_raw[2 * i])
                    lecture_count = len(buildings)

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

                    days = data[5].split()
                    majors = data[11].split(", ")

                    prerequisites = re.sub("veya", " or", data[12])
                    prerequisites.replace("(", "")
                    prerequisites.replace(")", "")
                    prerequisites_objects = []

                    if 'Yok/None' not in prerequisites and 'Diğer Şartlar' not in prerequisites and "Özel" not in prerequisites:
                        for prerequisite in prerequisites.split(' or '):
                            prerequisite = prerequisite.split()
                            course = " ".join([str(prerequisite) for prerequisite in prerequisite[:2]])
                            grade = str(prerequisite[-1])

                            prerequisites_objects.append(
                                Prerequisite.objects.get_or_create(code=course, min_grade=grade)[0])

                    if crn in crns:
                        course = Course.objects.get(crn=crn)
                        course.semester = semester
                        course.lecture_count = lecture_count
                        course.major_code = major_code
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
                        course = Course.objects.create(
                            semester=semester,
                            lecture_count=lecture_count,
                            major_code=major_code,
                            crn=crn,
                            catalogue=rows[1].contents[0]["href"],
                            code=data[1],
                            title=data[2],
                            instructor=data[3],
                            capacity=int(data[8]),
                            enrolled=int(data[9]),
                            reservation=data[10],
                            class_restriction=data[13],
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

                    for old_major in course.major_restriction.all():
                        course.major_restriction.remove(old_major)

                    for major in majors:
                        major_restriction, _ = MajorRestriction.objects.get_or_create(major=major)
                        course.major_restriction.add(major_restriction.major)

                    for prerequisite in prerequisites_objects:
                        course.prerequisites.add(prerequisite.id)

                    course.save()
                    nth_course += 1
                except AttributeError:
                    nth_course += 1
            except IndexError:
                break

        removed_crns = [crn for crn in active_crns if crn not in new_crns]
        for removed_crn in removed_crns:
            old_course = Course.objects.get(crn=removed_crn, semester=semester)
            old_course.active = False
            old_course.save()
            print("Course {} is removed from ITU SIS.".format(old_course))

        major_code.refreshed = timezone.now()
        major_code.save()
