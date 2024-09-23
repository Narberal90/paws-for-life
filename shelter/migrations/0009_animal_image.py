# Generated by Django 5.1.1 on 2024-09-22 19:16

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shelter", "0008_alter_user_phone_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="animal",
            name="image",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="image"
            ),
        ),
    ]
