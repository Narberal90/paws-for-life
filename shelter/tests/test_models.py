from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django.test import TestCase

from shelter.models import Animal, Adoption, Walk

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password",
            phone_number="+1234567890"
        )

    def test_user_str(self):
        self.assertEqual(str(self.user), self.user.username)


class AnimalModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password"
        )
        self.animal = Animal.objects.create(
            name="Buddy",
            age=3, type="dog",
            gender="boy",
            description="Friendly dog"
        )

    def test_animal_str(self):
        self.assertEqual(str(self.animal), "dog Buddy (boy)")

    def test_animal_age_cannot_be_negative(self):
        with self.assertRaises(ValidationError):
            Animal.objects.create(
                name="Negative Age",
                age=-1,
                type="cat",
                gender="girl",
                description="Invalid age",
            )

    def test_animal_name_cannot_be_empty(self):
        with self.assertRaises(ValidationError):
            Animal.objects.create(
                age=2,
                type="cat",
                gender="girl",
                description="No name"
            )


class AdoptionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password"
        )
        self.animal = Animal.objects.create(
            name="Buddy",
            age=3, type="dog",
            gender="boy",
            description="Friendly dog"
        )
        self.adoption = Adoption.objects.create(
            animal=self.animal,
            user=self.user
        )

    def test_adoption_str(self):
        self.assertIn("Adoption of Buddy", str(self.adoption))

    def test_unique_adoption_constraint(self):
        with transaction.atomic():
            with self.assertRaises(Exception):
                Adoption.objects.create(animal=self.animal, user=self.user)

        with transaction.atomic():
            new_animal = Animal.objects.create(
                name="Lucy",
                age=2,
                type="cat",
                gender="girl",
                description="Cute cat"
            )

        new_adoption = Adoption.objects.create(
            animal=new_animal,
            user=self.user
        )
        self.assertEqual(
            str(new_adoption),
            f"Adoption of Lucy by testuser on "
            f"{new_adoption.adoption_date}",
        )


class WalkModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password"
        )
        self.animal = Animal.objects.create(
            name="Buddy",
            age=3,
            type="dog",
            gender="boy",
            description="Friendly dog"
        )
        self.walk = Walk.objects.create(
            date="2024-09-30T10:00:00Z",
            description="Morning walk",
            user=self.user,
            animal=self.animal,
        )

    def test_walk_str(self):
        self.assertEqual(
            str(self.walk),
            "Walk scheduled on 2024-09-30T10:00:00Z")
