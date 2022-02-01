import regex as re
from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404
from django.test import TestCase
from requests_html import (
    HTMLSession,
    HTML,
)

from .models import (
    Course,
    Lecture,
    MajorCode,
    MajorRestriction,
    Prerequisite,
)


class ParserTestCase(TestCase):
    def setUp(self):
        self.BASE_URL = "http://www.sis.itu.edu.tr/tr/ders_programlari/LSprogramlar/prg.php?fb="
        session = HTMLSession()
        html = session.get(self.BASE_URL).html
        codes = html.find("select > option")
        for code in codes:
            if code.text != "":
                MajorCode.objects.create(code=code.text)

    def get_blg_courses(self):
        major_code = "ATA"
        major_code_obj = get_object_or_404(MajorCode, code=major_code)
        r = HTMLSession().get(self.BASE_URL + major_code)
        soup = BeautifulSoup(r.content, "html5lib")
        html = HTML(html=str(soup))
        table = html.find("table.dersprg", first=True)
        courses = table.find("tr")[2::]

        for course in courses:
            elements = course.find("td")
            catalogue = elements[1].absolute_links.pop()
            crn = elements[0].text
            code = elements[1].text
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
                    course = " ".join([str(prerequisite) for prerequisite in prerequisite[:2]])
                    grade = str(prerequisite[-1])

                    prerequisites_objects.append(
                        Prerequisite.objects.get_or_create(code=course, min_grade=grade)[0])

            capacity = int(elements[8].text)
            enrolled = int(elements[9].text)
            reservation = elements[10].text[:100]
            class_restriction = elements[13].text[:110]

            course_obj = Course.objects.create(
                lecture_count=lecture_count,
                major_code=major_code_obj,
                crn=crn,
                catalogue=catalogue,
                code=code,
                title=title,
                instructor=instructor,
                capacity=capacity,
                enrolled=enrolled,
                reservation=reservation,
                class_restriction=class_restriction,
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

            for major in restricted_majors:
                major_restriction, _ = MajorRestriction.objects.get_or_create(major=major)
                course_obj.major_restriction.add(major_restriction.major)

            for prerequisite in prerequisites_objects:
                course_obj.prerequisites.add(prerequisite.id)

            course_obj.save()
            print(course_obj)
