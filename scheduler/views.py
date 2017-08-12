from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.views import generic
from api.models import CourseCode, Course
from scheduler.models import Schedule


class IndexView(generic.ListView):
    model = Schedule
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context["my_schedule"] = user.my_schedule
            context["schedules"] = user.schedules.all()
            context["my_courses"] = user.courses.all()
        return context


class CoursesView(generic.DetailView):
    model = CourseCode
    slug_url_kwarg = "slug"
    template_name = "courses.html"

    def get_slug_field(self):
        return "code"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courses"] = context["object"].course_set.all()
        if self.request.user.is_authenticated:
            context["my_courses"] = [course.id for course in self.request.user.courses.all()]
        context["created"] = context["object"].created
        return context


class RegistrationView(generic.FormView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = "/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@login_required
def add_course(request):
    try:
        course_id = int(request.POST["course_id"])
        course = Course.objects.get(id=course_id)
        my_courses = request.user.courses
        if course in my_courses.all():
            my_courses.remove(course.id)
        else:
            my_courses.add(course.id)
        return JsonResponse({"courses": [course.crn for course in request.user.courses.all()], "successful": True})
    except Exception as error:
        return JsonResponse({"courses": [course.crn for course in request.user.courses.all()], "successful": False, "error": error})
