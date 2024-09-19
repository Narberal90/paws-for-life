from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class AnimalType(models.Model):
    name = models.CharField(max_length=50)


class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    description = models.TextField(default="unknown")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="events",
        on_delete=models.CASCADE)


class Animal(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('adopted', 'Adopted'),
        ('pending', 'Pending'),
        ('reserved', 'Reserved'),
    ]
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    type = models.ForeignKey(
        AnimalType,
        on_delete=models.CASCADE,
        related_name="animals")
    description = models.TextField(default="")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )
    admission_date = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(
        Event,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="animals"
    )

    # TODO: add photo = models.ImageField()
    class Meta:
        ordering = ("name",)
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['type']),
        ]

    def __str__(self):
        return f"{self.type.name} {self.name}"
