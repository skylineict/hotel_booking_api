# Generated by Django 5.0.3 on 2024-05-01 09:11

import django.db.models.deletion
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "id",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="abcdefghijklmnopqrstuvwxyz0123456789",
                        editable=False,
                        length=22,
                        max_length=16,
                        prefix="usr-",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("firstname", models.CharField(max_length=25)),
                ("lastname", models.CharField(max_length=25)),
                ("username", models.CharField(max_length=20, unique=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone", models.CharField(max_length=15, null=True, unique=True)),
                ("dob", models.DateField()),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("male", "Male"),
                            ("female", "Female"),
                            ("other", "Other"),
                        ],
                        max_length=10,
                    ),
                ),
                ("is_vendor", models.BooleanField(default=False)),
                ("email_verified", models.BooleanField(default=False)),
                ("phone_verified", models.BooleanField(default=False)),
                (
                    "verification_otp",
                    models.CharField(blank=True, max_length=6, null=True),
                ),
                ("verification_otp_expiration", models.DateTimeField(null=True)),
                (
                    "reset_password_otp",
                    models.CharField(blank=True, max_length=6, null=True),
                ),
                ("reset_password_otp_expiration", models.DateTimeField(null=True)),
                ("is_suspended", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
            },
        ),
        migrations.CreateModel(
            name="ResetPassword",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("reset_password_token", models.CharField(max_length=24)),
                ("expiration_time", models.DateTimeField()),
            ],
            options={
                "verbose_name": "reset_password",
            },
        ),
    ]
