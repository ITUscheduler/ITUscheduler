from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from api.models import CourseCode
from scheduler.models import Schedule


class IndexView(generic.ListView):
    model = Schedule
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["my_schedule"] = self.request.user.my_schedule
            context["schedules"] = self.request.user.schedules
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
        return context


class RegistrationView(generic.FormView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = "/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
