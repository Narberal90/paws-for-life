from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Walk, AnimalType, Animal, Adoption


@admin.register(User)
class UserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                    )
                },
            ),
        )
    )


@admin.register(AnimalType)
class AnimalTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "animal_count"]
    list_filter = ["name"]
    search_fields = ["name"]

    def animal_count(self, obj):
        return obj.animals.count()

    animal_count.short_description = "Number of Animals"


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "type",
        "age",
        "status",
        "admission_date",
        "walk",
    ]
    list_filter = ["type__name"]
    search_fields = [
        "name",
        "type__name",
        "age",
        "status",
    ]


@admin.register(Adoption)
class AdoptionAdmin(admin.ModelAdmin):
    list_display = ["animal", "user", "status", "adoption_date"]
    list_filter = ["status", "adoption_date"]
    search_fields = ["animal__name", "user__username"]


@admin.register(Walk)
class WalkAdmin(admin.ModelAdmin):
    list_display = ["name", "get_animals", "date", "user", "description"]

    def get_animals(self, obj):
        return ", ".join(animal.name for animal in obj.animals.all())

    get_animals.short_description = "Animals"
