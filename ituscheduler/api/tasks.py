import re

from bs4 import BeautifulSoup
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from django.shortcuts import get_object_or_404
from django.utils import timezone
from requests_html import (
    HTMLSession,
    HTML,
)

from .models import (
    Semester,
    MajorCode,
    Course,
    Prerequisite,
    MajorRestriction,
    Lecture,
)

BASE_URL = "https://www.sis.itu.edu.tr/TR/ogrenci/ders-programi/ders-programi.php?seviye=LS"


@shared_task(bind=True)
def refresh_courses(self, major_codes):
    progress_recorder = ProgressRecorder(self)
    major_codes_finished = []
    for code in major_codes:
        major_code = get_object_or_404(MajorCode, code=code)
        r = HTMLSession().post(
            url=BASE_URL,
            data={'seviye': 'LS', 'derskodu': code}
        )
        soup = BeautifulSoup(r.content, "html5lib")
        html = HTML(html=str(soup))
        semester = Semester.objects.current()

        # find table
        table = html.find("table.table.table-bordered.table-striped.table-hover.table-responsive", first=True)
        courses = table.find("tr")[2::]  # First two rows are table headers
        qs = Course.objects.filter(semester=semester, major_code=major_code)
        qs.update(active=False)

        # <tr class="table-baslik">
        #   <td>CRN</td> 0
        #   <td width="80">Course Code</td> 1
        #   <td>Course Title</td> 2
        #   <td>Teaching Method</td> 3
        #   <td>Instructor</td> 4
        #   <td>Building</td> 5
        #   <td>Day</td> 6
        #   <td>Time</td> 7
        #   <td>Room</td> 8
        #   <td>Capacity</td> 9
        #   <td><i>Enrolled</i></td> 10
        #   <td>Reservation<br>Maj./Cap./Enrl.</a></td> 11
        #   <td>Major Restriction</td> 12
        #   <td width="180">Prerequisites</td> 13
        #   <td>Class Rest.</td> 14
        # </tr>
        for course in courses:
            elements = course.find("td")
            catalogue = elements[1].absolute_links.pop()
            crn = elements[0].text
            course_code = elements[1].text
            title = elements[2].text
            teaching_method = elements[3].text
            instructor = elements[4].text

            try:
                buildings_raw = re.search("\">(.*)<br/>", elements[5].html).group(1)
            except AttributeError:
                buildings_raw = ""
            buildings = buildings_raw.split("<br/>")
            lecture_count = len(buildings)

            times_start = ""
            times_finish = ""
            for index in range(lecture_count):
                time = elements[7].full_text.split()[index].split("/")
                if "" in time or "----" in time:
                    time = ["2500", "2500"]
                for i in range(2):
                    if time[i][0] == "0":
                        time[i] = time[i][1::]
                times_start += time[0] + ","
                times_finish += time[1] + ","

            times_start = times_start[:-1:]
            times_finish = times_finish[:-1:]

            days = elements[6].text.split()
            restricted_majors = elements[12].text.split(", ")

            prerequisites = re.sub("veya", " or", elements[13].text)
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

            try:
                capacity = int(elements[9].text)
                enrolled = int(elements[10].text)
            except ValueError:
                capacity = 0
                enrolled = 0

            reservation = elements[11].text[:100]
            class_restriction = elements[14].text[:110]

            if Course.objects.filter(crn=crn).exists():
                course_obj = Course.objects.get(crn=crn)
                course_obj.semester = semester
                course_obj.lecture_count = lecture_count
                course_obj.major_code = major_code
                course_obj.catalogue = catalogue
                course_obj.code = course_code
                course_obj.title = title
                course_obj.teaching_method = teaching_method
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
                    teaching_method=teaching_method,
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
                room = elements[8].full_text.split()[i]

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
        major_codes_finished.append(major_code.code)
        progress_recorder.set_progress(len(major_codes_finished), len(major_codes))
