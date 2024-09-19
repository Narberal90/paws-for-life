from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone_number = PhoneNumberField(blank=True)

    def __str__(self):
        return self.username


class AnimalType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Walk(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    description = models.TextField(default="unknown")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="events",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Animal(models.Model):
    STATUS_CHOICES = [
        ("available", "Available"),
        ("adopted", "Adopted"),
        ("pending", "Pending"),
    ]
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    type = models.ForeignKey(
        AnimalType,
        on_delete=models.PROTECT,
        related_name="animals"
    )
    description = models.TextField(default="")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available"
    )
    admission_date = models.DateTimeField(auto_now_add=True)
    walk = models.ForeignKey(
        Walk,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="animals"
    )

    def clean(self):
        super().clean()
        if self.age < 0:
            raise ValidationError({'age': 'Age cannot be negative.'})
        if not self.name:
            raise ValidationError({'name': 'Name cannot be empty.'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    # TODO: add photo = models.ImageField()
    class Meta:
        ordering = ("name",)
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["type"]),
        ]

    def __str__(self):
        return f"{self.type.name} {self.name}"


class Adoption(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="adoptions"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="adoptions"
    )
    adoption_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("-adoption_date",)
        constraints = [
            models.UniqueConstraint(
                fields=["animal", "user"],
                name="unique_animal_user"
            )
        ]

    def __str__(self):
        return (f"Adoption of {self.animal.name} "
                f"by {self.user.username} on {self.adoption_date}")
