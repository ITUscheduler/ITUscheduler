from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.conf import settings
from api.models import MajorCode, Course, Semester
from scheduler.models import Schedule, Notification, ExtendedUser
from scheduler.forms import ScheduleForm, CustomUserCreationForm, ContactForm
from meta.views import MetadataMixin
from easy_pdf.views import PDFTemplateView
from easy_pdf.rendering import render_to_pdf
from pdf2image import convert_from_bytes
import numpy
from anytree import Node, RenderTree


# ---------------------- DENEMELER - SAÇMALAMALAR ----------------------
class Branch:
    matrix = numpy.full((10, 5), True)
    courses = []

    def extend_branch(self, course):
        # Check availability
        self.courses.append(course)


def schedule_generate(request):
    context = {}
    ex = Course.objects.filter(major_code_id="MAT")
    indexes = [0, 6, 20, 26, 38, 47, 55, 68, 73]
    courses = []
    for index in indexes:
        courses.append(ex[index])
    context["courses"] = courses

    main_node = Node(str(courses[0].crn), object=courses[0])

    tree_str = ""
    for pre, fill, node in RenderTree(main_node):
        tree_str += pre + node.name
    context["tree"] = tree_str

    return render(request, "schedule_generator.html", context)
# ---------------------- DENEMELER - SAÇMALAMALAR ----------------------


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


class ScheduleView(generic.DetailView):
    model = ExtendedUser
    slug_url_kwarg = "username"
    slug_field = "username"
    template_name = "share.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.object
        if self.object.my_schedule:
            context["has_schedule"] = True
        else:
            context["has_schedule"] = False

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
            Hour("17:30-18:29", 1730, 1829)
        ]
        context["hours"] = hours
        return context


class IndexView(MetadataMixin, generic.CreateView):
    form_class = ScheduleForm
    template_name = "index.html"

    title = 'ITU Scheduler'
    description = 'With ITU Scheduler you can browse up-to-date & detailed information about ITU courses and create possible course schedules with ease.'
    keywords = ['ITU', 'Scheduler', 'İTÜ', 'ITUscheduler', 'İTÜ Ders Programı', 'İTÜ Programcı', 'İTÜ Şenlikçi', 'dersler']
    url = '/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = self.request.user
        if user.is_authenticated:
            kwargs["courses"] = user.courses
            if self.request.method == "POST":
                post_data = kwargs["data"].copy()
                post_data["user"] = user.id
                kwargs["data"] = post_data
                if not kwargs["data"]:
                    return HttpResponseRedirect("/")
        return kwargs

    def form_valid(self, form):
        obj = form.save()
        self.request.user.my_schedule = obj
        self.request.user.save()
        courses = form.instance.courses
        overlapping_courses = []

        for _course in courses.all():
            if not _course.is_full():
                available, course = is_available(courses.all(), _course)
                if not available and (course, _course) not in overlapping_courses and (_course, course) not in overlapping_courses:
                    messages.warning(self.request, "Course #{} overlaps #{}. Your schedule is created anyway but please mind this.".format(course.crn, _course.crn, course.crn))
                    overlapping_courses.append((course, _course))
            else:
                msg = "Course {} is full, your schedule is created anyway but please mind this.".format(
                    _course.crn)
                notification = Notification()
                notification.user = self.request.user
                notification.msg = msg
                notification.save()

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
            Hour("17:30-18:29", 1730, 1829)
        ]
        context["hours"] = hours

        if user.is_authenticated:
            context["courses"] = user.courses.all()
            schedules = Schedule.objects.filter(user=user).all()
            context["schedules"] = schedules

            try:
                context["selected_schedule"] = schedules[0]
                if not user.my_schedule:
                    user.my_schedule = schedules[0]
            except IndexError:
                empty_schedule = Schedule()
                empty_schedule.id = 0
                context["selected_schedule"] = empty_schedule

            try:
                if not user.my_schedule:
                    raise AttributeError
                context["selected_schedule"] = user.my_schedule
                context["my_schedule"] = user.my_schedule
                context["my_courses"] = user.my_schedule.courses.all()
            except AttributeError:
                pass

            for schedule in schedules:
                if str(schedule.id) in self.request.path:
                    context["selected_schedule"] = schedule
                    break

            context["notifications"] = user.notification_set.all().filter(read=False)

        return context


@login_required
def schedule_export(request):
    if request.method == "POST":
        request.session["table_html"] = request.POST["table_html"]
        request.session["pdf_or_png"] = request.POST["pdf_or_png"]
        pdf_or_png = request.POST["pdf_or_png"]
        if pdf_or_png == "pdf":
            return HttpResponseRedirect("/schedule.pdf")
        elif pdf_or_png == "png":
            return HttpResponseRedirect("/schedule.png")
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")


class ScheduleExportView(PDFTemplateView):
    template_name = 'schedule.html'
    base_url = 'http://' + settings.STATIC_ROOT
    download_filename = 'ITUscheduler.pdf'
    pdf_or_png = "pdf"

    def get_context_data(self, **kwargs):
        context = super(ScheduleExportView, self).get_context_data(
            pagesize='A4 landscape',
            title='ITUscheduler',
            **kwargs
        )
        context["schedule_html"] = self.request.session.get("table_html")
        self.pdf_or_png = self.request.session.get("pdf_or_png")
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.pdf_or_png == "pdf":
            return self.render_to_response(context)
        elif self.pdf_or_png == "png":
            pdf = render_to_pdf("schedule.html", context=context, request=request, **kwargs)
            img = convert_from_bytes(pdf)[0]
            response = HttpResponse(content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename=ITUscheduler'
            img.save(response, "PNG")
            return response
        else:
            return HttpResponseRedirect("/")


class CoursesView(generic.ListView):
    model = Course
    template_name = "courses.html"

    def dispatch(self, request, *args, **kwargs):
        if not MajorCode.objects.all():
            return render(request, "courses.html")
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        user = self.request.user

        context = super().get_context_data(**kwargs)
        semester = user.my_semester if user.is_authenticated else Semester.objects.current()
        major_code = user.my_major_code if user.is_authenticated and user.my_major_code else MajorCode.objects.first()

        if self.request.GET.get("semester"):
            semester = Semester.objects.get(pk=self.request.GET["semester"])
        context["semester"] = semester

        if self.request.GET.get("major"):
            major_code = MajorCode.objects.get(pk=self.request.GET["major"])
        context["major"] = major_code

        courses = Course.objects.active().filter(
            semester=semester,
            major_code=major_code
        )

        codes = courses.order_by("code").values_list("code", flat=True).distinct()
        context["codes"] = codes
        if self.request.GET.get("code"):
            code = self.request.GET["code"]
            courses = courses.filter(code=code)
            context["code"] = code

        days = [("Pazartesi", "Monday"), ("Salı", "Tuesday"), ("Çarşamba", "Wednesday"), ("Perşembe", "Thursday"), ("Cuma", "Friday")]
        context["days"] = days
        if self.request.GET.get("day"):
            day = self.request.GET["day"]
            courses = courses.filter(lecture__day=day).distinct()
            context["day"] = day

        for course in courses:
            course.times = []
            for lecture in course.lecture_set.all():
                course.times.append("{}/{} ".format(lecture.time_start, lecture.time_finish))
        context["courses"] = courses
        context["refreshed"] = major_code.refreshed if major_code else None

        if user.is_authenticated:
            context["my_courses"] = user.courses.all().values_list("crn", flat=True)
            user.my_semester = semester
            user.my_major_code = major_code
            user.save()

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


def contact(request):
    form_class = ContactForm
    if request.method == "POST":
        form = form_class(data=request.POST)
        if form.is_valid():
            subject = "[ITUscheduler] | " + form.cleaned_data['name']
            message = form.cleaned_data['message']
            reply_to = [form.cleaned_data['email']]
            sender = "info@ituscheduler.com"
            recipients = ['info@ituscheduler.com', 'doruk@gezici.me', 'altunerism@gmail.com']
            cc_myself = True  # form.cleaned_data['cc_myself']
            if cc_myself:
                recipients.extend(reply_to)
            msg = EmailMessage(subject, message, sender, recipients, reply_to=reply_to)
            msg.send()
        return render(request, 'contact.html', {
            'form': form,
            'successful': True
        })
    return render(request, 'contact.html', {
        'form': form_class
    })


def privacy_policy(request):
    return render(request, 'privacypolicy.htm')


@login_required
def remove_my_courses(request):
    try:
        request.user.courses.clear()
        return JsonResponse({"successful": True})
    except Exception as error:
        return JsonResponse({"successful": False, "error": error})


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
        return JsonResponse({"successful": True})
    except Exception as error:
        return JsonResponse({"successful": False, "error": error})


@login_required
def select_schedule(request):
    try:
        schedule_id = int(request.POST["schedule_id"])
        schedule = Schedule.objects.get(id=schedule_id)
        if request.user == schedule.user:
            request.user.my_schedule = schedule
            request.user.save()
        else:
            raise Exception("You are not authorized to select that schedule.")
    except Exception as error:
        return JsonResponse({"successful": False, "error": str(error)})
    return JsonResponse({"successful": True, "scheduleId": schedule_id})


@login_required
def delete_schedule(request):
    try:
        schedule_id = int(request.POST["schedule_id"])
        schedule = Schedule.objects.get(id=schedule_id)
        if request.user == schedule.user:
            schedule.delete()
        else:
            raise Exception("You are not authorized to delete that schedule.")
    except Exception as error:
        return JsonResponse({"successful": False, "error": str(error)})
    return JsonResponse({"successful": True, "scheduleId": schedule_id})
