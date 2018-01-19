from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from scheduler.models import Schedule


class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(
        required=True,
        widget=forms.Textarea
    )


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Your ITU email address')

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email')

    def clean_email(self):
        data = self.cleaned_data['email']
        if '@itu.edu.tr' != data[-11:]:
            raise forms.ValidationError('This is not a valid ITU email address!')
        return data


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
