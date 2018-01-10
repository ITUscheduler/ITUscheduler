from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.views import generic
from django.contrib import messages
from api.models import CourseCode, Course
from scheduler.models import Schedule
from scheduler.forms import ScheduleForm, CustomUserCreationForm


def is_available(courses, course):
    if course.is_full():
        return False, ""
    for c in courses:
        if c != course:
            for l in c.lecture_set.all():
                for lecture in course.lecture_set.all():
                    if l.day == lecture.day:
                        if lecture.time_start <= l.time_start <= lecture.time_finish or lecture.time_finish <= l.time_finish <= lecture.time_finish:
                            return False, c
                        else:
                            continue
    return True, ""

# def fit(courses, problematic):
#     unremovable_courses = []
#     will_be_replaced = []
#
#     possible_replacements = [(course, Course.objects.filter(course_code=course.course_code)) for course, _ in problematic]
#
#     while len(possible_replacements) > 0:
#
#         #if not possible_replacements:
#         #    possible_replacements = [(course, Course.objects.filter(course_code=course.course_code)) for course in courses]
#
#         for replaceble, replacements in possible_replacements:
#             if len(replacements) <= 1:
#                 possible_replacements.remove((replaceble, replacements))
#
#
#         for replaceble, replacements in possible_replacements:
#             quit = True
#             for replacement in replacements:
#                 copy = courses
#                 list(copy).remove(replaceble)
#                 available, _ = is_available(copy, replacement)
#
#                 if available:
#                     list(copy).append(replacement)
#                     courses = copy
#                     possible_replacements.remove((replaceble, replacements))
#                     quit = False
#
#             if quit:
#                 possible_replacements.remove((replaceble, replacements))
#                 unremovable_courses.append(replaceble)
#
#
#     return courses
#


class IndexView(generic.CreateView):
    form_class = ScheduleForm
    template_name = "index.html"
    success_url = "."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = self.request.user
        if user.is_authenticated:
            kwargs["courses"] = user.courses
            _ = [
                "8:30-9:29",
                "9:30-10:29",
                "10:30-11:29",
                "11:30-12:29",
                "12:30-13:29",
                "13:30-14:29",
                "14:30-15:29",
                "15:30-16:29",
                "16:30-17:29",
                "17:30-18:29",
                "18:30-19:29",
                "19:30-20:29"
            ]
            if self.request.method == "POST":
                post_data = kwargs["data"].copy()
                post_data["user"] = user.id
                kwargs["data"] = post_data
        return kwargs

    def form_valid(self, form):
        form.save()
        courses = form.instance.courses
        #problematic = [(course, is_available(courses.all(), course)[1]) for course in courses.all() if
        #               not is_available(courses.all(), course)[0]]
        #fitted_courses = fit(courses.all(), problematic)
        return_back = False
        overlaping_courses = []

        for _course in courses.all():
            available, course = is_available(courses.all(), _course)
            if not available and (course, _course) not in overlaping_courses and (_course, course) not in overlaping_courses:
                messages.warning(self.request, "Course #{} overlaps #{}. Please choose another one.".format(course.crn, _course.crn, course.crn))
                overlaping_courses.append((course, _course))
                return_back = True


        if return_back:
            return self.form_invalid(form)

        return super(IndexView, self).form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        class Hour:
            def __init__(self, time, time_start, time_finish, course=None):
                self.time = time
                self.time_start = time_start
                self.time_finish = time_finish
                try:
                    day = str(course.day).lower()
                    self.day = {day: "#{} {}".format(course.crn, course.code)}
                except AttributeError:
                    self.day = {}

        hours = [
            Hour("8:30-9:29", 830, 929),
            Hour("9:30-10:29", 930, 1029),
            Hour("10:30-11:29", 1030, 1129),
            Hour("11:30-12:29", 1130, 1229),
            Hour("12:30-13:29", 1230, 1329),
            Hour("13:30-14:29", 1330, 1429),
            Hour("14:30-15:29", 1430, 1529),
            Hour("15:30-16:29", 1530, 1629),
            Hour("16:30-17:29", 1630, 1729),
            Hour("17:30-18:29", 1730, 1829),
            Hour("18:30-19:29", 1830, 1929),
            Hour("19:30-20:29", 1930, 2029),
            Hour("20:30-21:29", 2030, 2129)
        ]
        context["hours"] = hours

        if user.is_authenticated:
            context["courses"] = user.courses.all()
            schedules = Schedule.objects.filter(user=user).all()
            context["schedules"] = schedules
            context["my_schedule"] = user.my_schedule
            context["my_courses"] = user.my_schedule.courses.all()

            try:
                context["selected_schedule"] = schedules[0]
            except IndexError:
                empty_schedule = Schedule()
                empty_schedule.id = 0
                context["selected_schedule"] = empty_schedule

            try:
                if not user.my_schedule:
                    raise AttributeError
                context["selected_schedule"] = user.my_schedule
            except AttributeError:
                pass

            for schedule in schedules:
                if str(schedule.id) in self.request.path:
                    context["selected_schedule"] = schedule
                    break

        return context


class CoursesView(generic.DetailView):
    model = CourseCode
    slug_url_kwarg = "slug"
    template_name = "courses.html"

    def get_slug_field(self):
        return "code"

    def dispatch(self, request, *args, **kwargs):
        if not CourseCode.objects.all() or not Course.objects.filter(course_code=kwargs["slug"]).all():
            return render_to_response("courses.html", context={"request": request, "user": request.user, "course_codes": CourseCode.objects.all()})
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course_codes"] = CourseCode.objects.all()

        context["codes"] = []
        for course in context["object"].course_set.all():
            if course.code not in context["codes"]:
                context["codes"].append(course.code)

        courses = context["object"].course_set.all()

        if self.request.GET.get("query"):
            code = self.request.GET["query"]
            courses = context["object"].course_set.filter(code=code)
            context["query"] = code


        for course in courses:
            course.times = []
            for i in range(course.lecture_count):
                lectures = course.lecture_set.all()
                course.times.append("{}/{} ".format(lectures[i].time_start, lectures[i].time_finish))
        context["courses"] = courses


        if self.request.user.is_authenticated:
            context["my_courses"] = [course.crn for course in self.request.user.courses.all()]
        context["refreshed"] = context["object"].refreshed
        return context


class RegistrationView(generic.FormView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = "/"

    def form_valid(self, form):
        form.save()
        user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
        login(self.request, user)
        return super().form_valid(form)


@login_required
def add_course(request):
    try:
        course_crn = int(request.POST["course_crn"])
        course = Course.objects.get(crn=course_crn)
        my_courses = request.user.courses
        if course in my_courses.all():
            my_courses.remove(course.crn)
        else:
            my_courses.add(course.crn)
        return JsonResponse({"courses": [course.crn for course in request.user.courses.all()], "successful": True})
    except Exception as error:
        return JsonResponse({"courses": [course.crn for course in request.user.courses.all()], "successful": False, "error": error})


@login_required
def select_schedule(request):
    try:
        schedule_id = int(request.POST["schedule_id"])
        schedule = Schedule.objects.get(id=schedule_id)
        request.user.my_schedule = schedule
        request.user.save()
    except Exception as error:
        return JsonResponse({"successful": False, "error": str(error)})
    return JsonResponse({"successful": True, "scheduleId": schedule_id})
