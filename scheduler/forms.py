from django import forms
from scheduler.models import Schedule


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
