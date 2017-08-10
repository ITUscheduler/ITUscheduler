import requests, sys
from bs4 import BeautifulSoup

BASE_URL = "http://www.sis.itu.edu.tr/tr/ders_programlari/LSprogramlar/prg.php?fb="


class Data:
    options = []
    courses = []


class Course:
    count = 1
    def is_full(self):
        if self.enrolled < self.capacity:
            return False
        else:
            return True

    def __init__(self, data, i=0):
        self.crn = data[0]
        self.code = data[1]
        self.title = data[2]
        self.instructor = data[3]
        self.count = len(data[4]) // 3
        self.building = data[4][3*i:3*i+3:]
        self.day = data[5].split()[i]
        time = data[6][:-1:].split()[i].split("/")
        if "" in time:
            time = ["-1", "-1"]
        for index, t in enumerate(time):
            if t[0] == "0":
                time[index] = t[1::]
        self.time = [int(time[0]), int(time[1])]
        self.room = data[7].split()[i]
        self.capacity = int(data[8])
        self.enrolled = int(data[9])
        self.reservation = data[10]
        self.major_restriction = data[11]
        self.prerequisites = data[12]
        self.class_restriction = data[13]

    def __str__(self):
        return self.crn + " " + self.code + " " + self.title + " | " + self.instructor + " " + self.building + ":" + self.room + " " + self.day + " " + str(self.time[0]) + "/" + str(self.time[1]) + " | " + str(self.enrolled) + "/" + str(self.capacity)


class Schedule:
    courses = []

    def is_available(self, course):
        if course.is_full():
            return False
        for c in self.courses:
            if course.day == c.day and c.time[0] <= course.time[0] <= c.time[1] or c.time[0] <= course.time[1] <= c.time[1]:
                return False
            else:
                continue
        return True

r = requests.get(BASE_URL)
soup = BeautifulSoup(r.content, "html.parser")

for option in soup.find("select").find_all("option"):
    if option.attrs["value"] != "":
        Data.options.append(option.get_text()[:-1:])

print("-" * 80)
bee_ascii = """
              \     /
          \    o ^ o    /
            \ (     ) /
 ____________(%%%%%%%)____________
(     /   /  )%%%%%%%(  \   \     )
(___/___/__/           \__\___\___)     ITU Scheduler
   (     /  /(%%%%%%%)\  \     )        github @dorukgezici
    (__/___/ (%%%%%%%) \___\__)
            /(       )\\
          /   (%%%%%)   \\
               (%%%)
                 !
"""
print(bee_ascii)
print("-" * 80)
print("Course Codes")
print("-" * 80)

for i in range(0, len(Data.options), 20):
    for j in range(i, i+20):
        try:
            print(Data.options[j], end=" ")
        except:
            pass
    print()

print("-" * 80)
option = str(input("Select Course Code: ")).upper()
if option not in Data.options:
    sys.exit("Wrong Course Code!")
print("-" * 80)
r = requests.get(BASE_URL + option)
soup = BeautifulSoup(r.content, "html.parser")

i = 5
while True:
    try:
        raw_course = soup.select_one("tr:nth-of-type({})".format(i))
        try:
            data = [row.get_text() for row in raw_course.find_all("td")]
            count = len(data[4]) // 3
            for index in range(count):
                Data.courses.append(Course(data, index))
            i += 1
        except AttributeError as error:
            i += 1
            pass
    except IndexError as error:
        break

print("Courses")
print("-" * 80)
for index, course in enumerate(Data.courses):
    print("#" + str(index), course)
print("-" * 80)
selected_ids = [int(splitted) for splitted in str(input("Enter selected courses with IDs(#), select multiple using commas: ")).split(",")]
print("-" * 80)

schedule = Schedule()
for c_id in selected_ids:
    course = Data.courses[c_id]
    if schedule.is_available(course):
        schedule.courses.append(course)

for course in schedule.courses:
    print(course)
