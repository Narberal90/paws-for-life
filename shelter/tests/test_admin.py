from django.contrib import admin
from django.test import TestCase

from shelter.admin import UserAdmin, AnimalAdmin, AdoptionAdmin, WalkAdmin
from shelter.models import User, Animal, Adoption, Walk


class AdminSiteTest(TestCase):
    def test_user_admin_registered(self):
        self.assertTrue(admin.site.is_registered(User))
        self.assertIsInstance(admin.site._registry[User], UserAdmin)

    def test_animal_admin_registered(self):
        self.assertTrue(admin.site.is_registered(Animal))
        self.assertIsInstance(admin.site._registry[Animal], AnimalAdmin)

    def test_adoption_admin_registered(self):
        self.assertTrue(admin.site.is_registered(Adoption))
        self.assertIsInstance(admin.site._registry[Adoption], AdoptionAdmin)

    def test_walk_admin_registered(self):
        self.assertTrue(admin.site.is_registered(Walk))
        self.assertIsInstance(admin.site._registry[Walk], WalkAdmin)

    def test_user_admin_list_display(self):
        self.assertIn("phone_number", UserAdmin.list_display)

    def test_animal_admin_list_display(self):
        self.assertEqual(
            AnimalAdmin.list_display,
            [
                "name",
                "type",
                "gender",
                "age",
                "status",
                "admission_date",
                "walk",
            ],
        )

    def test_adoption_admin_list_display(self):
        self.assertIn(
            "get_user_number",
            AdoptionAdmin.list_display
        )

    def test_walk_admin_list_display(self):
        self.assertEqual(
            WalkAdmin.list_display,
            ["animal", "date", "user", "description"],
        )

    def test_animal_admin_list_filter(self):
        self.assertEqual(
            AnimalAdmin.list_filter,
            ["type", "gender"]
        )

    def test_adoption_admin_list_filter(self):
        self.assertEqual(
            AdoptionAdmin.list_filter,
            ["status", "adoption_date"]
        )

    def test_animal_admin_search_fields(self):
        self.assertEqual(
            AnimalAdmin.search_fields,
            ["name", "type", "gender", "age", "status"],
        )

    def test_adoption_admin_search_fields(self):
        self.assertEqual(
            AdoptionAdmin.search_fields,
            ["animal__name", "user__username"]
        )
