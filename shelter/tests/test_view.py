from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from shelter.models import Animal

User = get_user_model()


class HomePageViewTest(TestCase):
    def test_home_page_view(self):
        """Test the home page view context data."""
        Animal.objects.create(
            name="Test Dog",
            type="dog",
            status="available",
            age=3
        )
        response = self.client.get(reverse("shelter:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "shelter/home.html"
        )
        self.assertIn("total_animals", response.context)
        self.assertIn("adopted_count", response.context)
        self.assertIn("available_count", response.context)


class AnimalListViewTest(TestCase):
    def test_animal_list_view(self):
        """Test the animal list view with filtering options."""
        Animal.objects.create(
            name="Test Cat",
            type="cat",
            status="available",
            age=2
        )
        response = self.client.get(
            reverse(
                "shelter:animals-list-for-adoption"
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "shelter/animals_list_for_adoption.html"
        )
        self.assertEqual(len(response.context["animal_list"]), 1)


class DogListViewTest(TestCase):
    def test_dog_list_view(self):
        """Test the dog list view displays only available dogs."""
        Animal.objects.create(
            name="Test Dog",
            type="dog",
            status="available",
            age=3
        )
        Animal.objects.create(
            name="Test Dog_two",
            type="dog",
            status="adopted",
            age=3
        )
        response = self.client.get(
            reverse(
                "shelter:dog-list"
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "shelter/dog_list.html"
        )
        self.assertEqual(len(response.context["animal_list"]), 1)


class ScheduleWalkViewTest(TestCase):
    def setUp(self):
        """Set up a user and dog for walk scheduling tests."""
        self.user = User.objects.create_user(
            username="testuser",
            password="password"
        )
        self.dog = Animal.objects.create(
            name="Test Dog",
            type="dog",
            status="available",
            age=1
        )

    def test_redirect_if_not_logged_in(self):
        """Test if unauthenticated users are redirected to login page."""
        response = self.client.get(
            reverse(
                "shelter:schedule-walk",
                kwargs={"dog_pk": self.dog.pk}
            )
        )
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/schedule-walk/"
            f"{self.dog.pk}/"
        )

    def test_logged_in_user_can_schedule_walk(self):
        """Test if a logged-in user can schedule a walk."""
        self.client.login(
            username="testuser",
            password="password"
        )
        response = self.client.post(
            reverse(
                "shelter:schedule-walk",
                kwargs={"dog_pk": self.dog.pk}
            ),
            {"date": "2024-09-30T10:00:00Z", "description": "Test walk"},
        )
        self.assertEqual(response.status_code, 302)


class AdoptionCreateViewTest(TestCase):
    def setUp(self):
        """Set up a user and animal for adoption tests."""
        self.user = User.objects.create_user(
            username="testuser",
            password="password",
            phone_number="1234567890"
        )
        self.animal = Animal.objects.create(
            name="Test Cat",
            type="cat",
            status="available",
            age=5
        )

    def test_redirect_if_not_logged_in(self):
        """
        Test if unauthenticated users
        are redirected to login page for adoption.
        """
        response = self.client.get(
            reverse(
                "shelter:adoption-create",
                kwargs={"animal_pk": self.animal.pk}
            )
        )
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/adopt/"
            f"{self.animal.pk}/"
        )

    def test_adoption_request_submission(self):
        """Test if logged-in users can submit an adoption request."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse(
                "shelter:adoption-create",
                kwargs={"animal_pk": self.animal.pk}
            ),
            {"adoption_date": "2024-09-30"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("shelter:success-adoption"))


class CustomLoginViewTest(TestCase):
    def test_login_view(self):
        """Test the custom login view functionality."""
        User.objects.create_user(
            username="testuser",
            password="password"
        )
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "password"}
        )
        self.assertEqual(response.status_code, 302)


class CustomLogoutViewTest(TestCase):
    def setUp(self):
        """Set up a user for logout testing."""
        self.user = User.objects.create_user(
            username="testuser",
            password="password"
        )

    def test_logout_view(self):
        """Test the custom logout view functionality."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/logged_out.html")
