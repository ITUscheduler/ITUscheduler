from __future__ import absolute_import, unicode_literals
from django.utils import timezone
from bs4 import BeautifulSoup
from celery import shared_task
from django.shortcuts import get_object_or_404
from api.models import Semester, MajorCode, Course, Prerequisite, MajorRestriction, Lecture
from requests_html import HTMLSession, HTML
import re

BASE_URL = "http://www.sis.itu.edu.tr/tr/ders_programlari/LSprogramlar/prg.php?fb="


@shared_task(bind=True)
def refresh_courses(self, major_codes):
    export_from_file = False
    htmls = {}

    for code in major_codes:
        major_code = get_object_or_404(MajorCode, code=code)

        if export_from_file:
            html = htmls[code]
            semester_html = html.find("span.ustbaslik", first=True).text
            semester = ""
            for semester_code, semester_txt in Semester.SEMESTER_CHOICES_TURKISH:
                if semester_html in semester_txt:
                    semester = semester_code
                    break
            if semester == "":
                # Means there is something wrong with my approach to semester. Needs to be revisited
                print("Semester could not be found.")
            semester, _ = Semester.objects.get_or_create(name=semester)
        else:
            r = HTMLSession().get(BASE_URL + code)
            soup = BeautifulSoup(r.content, "html5lib")
            html = HTML(html=str(soup))
            semester = Semester.objects.current()

        table = html.find("table.dersprg", first=True)
        courses = table.find("tr")[2::]  # First two rows are table headers
        qs = Course.objects.filter(semester=semester, major_code=major_code)
        qs.update(active=False)

        for course in courses:
            elements = course.find("td")
            catalogue = elements[1].absolute_links.pop()
            crn = elements[0].text
            course_code = elements[1].text
            title = elements[2].text
            instructor = elements[3].text

            buildings_raw = re.search("\">(.*)<br/>", elements[4].html).group(1)
            buildings = buildings_raw.split("<br/>")
            lecture_count = len(buildings)

            times_start = ""
            times_finish = ""
            for index in range(lecture_count):
                time = elements[6].full_text.split()[index].split("/")
                if "" in time or "----" in time:
                    time = ["2500", "2500"]
                for i in range(2):
                    if time[i][0] == "0":
                        time[i] = time[i][1::]
                times_start += time[0] + ","
                times_finish += time[1] + ","

            times_start = times_start[:-1:]
            times_finish = times_finish[:-1:]

            days = elements[5].text.split()
            restricted_majors = elements[11].text.split(", ")

            prerequisites = re.sub("veya", " or", elements[12].text)
            prerequisites.replace("(", "")
            prerequisites.replace(")", "")
            prerequisites_objects = []
            if 'Yok/None' not in prerequisites and 'Diğer Şartlar' not in prerequisites and "Özel" not in prerequisites:
                for prerequisite in prerequisites.split(' or '):
                    prerequisite = prerequisite.split()
                    if not prerequisite:
                        continue
                    course = " ".join([str(prerequisite) for prerequisite in prerequisite[:2]])
                    grade = str(prerequisite[-1])

                    prerequisites_objects.append(
                        Prerequisite.objects.get_or_create(code=course, min_grade=grade)[0])

            capacity = int(elements[8].text)
            enrolled = int(elements[9].text)
            reservation = elements[10].text[:100]
            class_restriction = elements[13].text[:110]

            if Course.objects.filter(crn=crn).exists():
                course_obj = Course.objects.get(crn=crn)
                course_obj.semester = semester
                course_obj.lecture_count = lecture_count
                course_obj.major_code = major_code
                course_obj.catalogue = catalogue
                course_obj.code = course_code
                course_obj.title = title
                course_obj.instructor = instructor
                course_obj.capacity = capacity
                course_obj.enrolled = enrolled
                course_obj.reservation = reservation
                course_obj.class_restriction = class_restriction
                course_obj.active = True

                course_obj.save()

                for lecture in course_obj.lecture_set.all():
                    lecture.delete()
            else:
                course_obj = Course.objects.create(
                    semester=semester,
                    lecture_count=lecture_count,
                    major_code=major_code,
                    crn=crn,
                    catalogue=catalogue,
                    code=course_code,
                    title=title,
                    instructor=instructor,
                    capacity=capacity,
                    enrolled=enrolled,
                    reservation=reservation,
                    class_restriction=class_restriction,
                    active=True
                )

            for i in range(lecture_count):
                time_start = times_start.split(",")[i]
                time_finish = times_finish.split(",")[i]
                room = elements[7].full_text.split()[i]

                Lecture.objects.create(
                    building=buildings[i],
                    day=days[i],
                    time_start=time_start,
                    time_finish=time_finish,
                    room=room,
                    course=course_obj
                )

            for old_major in course_obj.major_restriction.all():
                course_obj.major_restriction.remove(old_major)

            for major in restricted_majors:
                major_restriction, _ = MajorRestriction.objects.get_or_create(major=major)
                course_obj.major_restriction.add(major_restriction.major)

            for prerequisite in prerequisites_objects:
                course_obj.prerequisites.add(prerequisite.id)

            course_obj.save()
            print(course_obj)
            continue

        major_code.refreshed = timezone.now()
        major_code.save()
