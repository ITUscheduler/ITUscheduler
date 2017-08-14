from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from scheduler.models import Schedule


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()


class ScheduleForm(forms.ModelForm):
    def __init__(self, courses=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if courses is not None:
            self.fields["courses"].queryset = courses

    class Meta:
        model = Schedule
        exclude = []
        widgets = {
            "user": forms.HiddenInput()
        }
