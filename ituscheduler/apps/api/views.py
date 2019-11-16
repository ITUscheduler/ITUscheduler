from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from requests_html import HTMLSession, HTML
from .models import MajorCode, Course, Prerequisite, MajorRestriction
from ..scheduler.models import Schedule
from celery.result import AsyncResult
from .tasks import refresh_courses


BASE_URL = "http://www.sis.itu.edu.tr/tr/ders_programlari/LSprogramlar/prg.php?fb="


class RefreshCoursesView(UserPassesTestMixin, generic.ListView):
    model = MajorCode
    template_name = "refresh_courses.html"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False


@user_passes_test(lambda u: u.is_superuser)
def db_refresh_major_codes(request):
    session = HTMLSession()
    html: HTML = session.get(BASE_URL).html

    html_response = "<a href='/'><h1>Major Codes refreshed!</h1></a>"
    codes = [major_code.code for major_code in MajorCode.objects.all()]
    options = html.find("select > option")[1:]

    for option in options:
        opt = option.text
        if opt != "":
            if opt in codes:
                codes.remove(opt)
            query = MajorCode.objects.filter(code=opt)
            if not query.exists():
                MajorCode.objects.create(code=opt)
                html_response += "<p>{} added</p>".format(opt)

    # Check if any major_code is removed from SIS
    if options:
        for code in codes:
            major_code = MajorCode.objects.get(code=code)
            # major_code.delete()
            html_response += "<p>ATTENTION! {} is removed from SIS</p>".format(major_code)
    return HttpResponse(html_response)


@csrf_exempt
@user_passes_test(lambda u: u.is_superuser)
def db_refresh_courses(request):
    major_codes = request.POST.getlist("major_codes[]")
    task_id = refresh_courses.delay(major_codes)
    return redirect("task_status", task_id=task_id)


class TaskStatusView(UserPassesTestMixin, generic.TemplateView):
    template_name = "task_status.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = AsyncResult(self.kwargs["task_id"])
        context["task"] = task
        return context

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False


class FlushView(UserPassesTestMixin, generic.TemplateView):
    model = MajorCode
    template_name = "flush.html"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False


@user_passes_test(lambda u: u.is_superuser)
def db_flush(request):
    MajorCode.objects.all().delete()
    Course.objects.all().delete()
    Schedule.objects.all().delete()
    MajorRestriction.objects.all().delete()
    Prerequisite.objects.all().delete()
    return HttpResponse("<a href='/'><h1>Major Codes and Courses flushed!</h1></a>")
