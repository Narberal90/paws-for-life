from django.test import TestCase
from django.utils import timezone
from shelter.forms import (
    WalkScheduleForm,
    AdoptionForm,
    CustomUserCreationForm,
    UserProfileForm,
)


class WalkScheduleFormTest(TestCase):
    def test_date_field_constraints(self):
        form = WalkScheduleForm()
        today = timezone.now().date()
        tomorrow = today + timezone.timedelta(days=1)
        self.assertEqual(
            form.fields["date"]
            .widget.attrs["min"],
            f"{today}T10:00"
        )
        self.assertEqual(
            form.fields["date"]
            .widget.attrs["max"],
            f"{tomorrow}T17:00"
        )

    def test_valid_data(self):
        form_data = {
            "date": timezone.now() + timezone.timedelta(hours=1),
            "description": "Walking the dog",
        }
        form = WalkScheduleForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_past_date(self):
        form_data = {
            "date": timezone.now() - timezone.timedelta(days=1),
            "description": "Walking the dog",
        }
        form = WalkScheduleForm(data=form_data)
        self.assertFalse(form.is_valid())


class AdoptionFormTest(TestCase):
    def test_adoption_form_valid(self):
        form_data = {
            "notes": "I love this pet and would like to adopt."
        }
        form = AdoptionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_adoption_form_empty_notes(self):
        form_data = {"notes": ""}
        form = AdoptionForm(data=form_data)
        self.assertTrue(
            form.is_valid(),
            "Form should be valid even with empty notes"
        )


class CustomUserCreationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            "username": "testuser",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123",
            "phone_number": "+380933456789",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_phone_number(self):
        form_data = {
            "username": "testuser",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123",
            "phone_number": "invalid_phone",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_password(self):
        form_data = {
            "username": "testuser",
            "password1": "1111",
            "password2": "1111",
            "phone_number": "+380933456789",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserProfileFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            "username": "testuser",
            "first_name": "Narberal",
            "last_name": "Gamma",
            "phone_number": "+380733456789",
        }
        form = UserProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_username(self):
        form_data = {
            "first_name": "Narberal",
            "last_name": "Gamma",
            "phone_number": "+380733456789",
        }
        form = UserProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
