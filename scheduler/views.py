from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from api.models import Course


class IndexView(generic.ListView):
    model = Course
    template_name = "index.html"


class RegistrationView(generic.FormView):
    form_class = UserCreationForm
    template_name = "signup.html"
    success_url = "/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
