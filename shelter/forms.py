from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from phonenumber_field.formfields import PhoneNumberField

from .models import Walk, Adoption


class WalkScheduleForm(forms.ModelForm):
    class Meta:
        model = Walk
        fields = ["date", "description"]
        widgets = {
            "date": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.now().date()
        tomorrow = today + timezone.timedelta(days=1)
        self.fields["date"].widget.attrs["min"] = f"{today}T10:00"
        self.fields["date"].widget.attrs["max"] = f"{tomorrow}T17:00"

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date:
            if date < timezone.now():
                raise ValidationError("The date cannot be in the past.")

            if date.hour < 10 or date.hour > 17:
                raise ValidationError(
                    "Please select a time between 10:00 and 17:00."
                )

        return date


class AdoptionForm(forms.ModelForm):
    class Meta:
        model = Adoption
        fields = ["notes"]
        widgets = {
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter your message (optional)",
                }
            ),
        }


# User custom form


class CustomUserCreationForm(UserCreationForm):
    phone_number = PhoneNumberField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "For pet adoption"}
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "phone_number", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})


# Login form


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["password"].widget.attrs.update({"class": "form-control"})


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "phone_number", "first_name", "last_name"]
        widgets = {
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your phone number"
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your first name"
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your last name"
                }
            ),
        }
