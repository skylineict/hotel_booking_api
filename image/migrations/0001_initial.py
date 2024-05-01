# Generated by Django 5.0.3 on 2024-05-01 11:07

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    cloudinary.models.CloudinaryField(
                        max_length=255, verbose_name="image"
                    ),
                ),
            ],
            options={
                "verbose_name": "image",
                "verbose_name_plural": "images",
            },
        ),
    ]
