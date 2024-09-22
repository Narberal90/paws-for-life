from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Walk, Animal, Adoption


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("phone_number",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("phone_number",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "phone_number",
                    )
                },
            ),
        )
    )


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "type",
        "gender",
        "age",
        "status",
        "admission_date",
        "walk",
    ]
    list_filter = ["type", "gender"]
    search_fields = [
        "name",
        "type",
        "gender",
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
    list_display = ["animal", "date", "user", "description"]
    fields = ["date", "user", "description", "animal"]
