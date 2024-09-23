from django.contrib.auth import get_user_model
from django.test import TestCase
from shelter.models import Adoption, Animal


class AdoptionSignalTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.animal = Animal.objects.create(
            name="Murchyk",
            status="available",
            age=1
        )
        self.adoption = Adoption.objects.create(
            animal=self.animal, status="pending", user=self.user
        )

    def test_signal_on_adoption_pending(self):
        self.adoption.status = "pending"
        self.adoption.save()
        self.animal.refresh_from_db()
        self.assertEqual(self.animal.status, "pending")

    def test_signal_on_adoption_approved(self):
        self.adoption.status = "approved"
        self.adoption.save()
        self.animal.refresh_from_db()
        self.assertEqual(self.animal.status, "adopted")

    def test_signal_on_adoption_rejected(self):
        self.adoption.status = "rejected"
        self.adoption.save()
        self.animal.refresh_from_db()
        self.assertEqual(self.animal.status, "available")
