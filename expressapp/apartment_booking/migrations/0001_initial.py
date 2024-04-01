# Generated by Django 5.0.3 on 2024-03-31 15:35

import django.db.models.deletion
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('apartment', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ApartmentBooking',
            fields=[
                ('booking_id', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnopqrstuvwxyz0123456789', editable=False, length=12, max_length=20, prefix='', primary_key=True, serialize=False, unique=True)),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('date_booked', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('salutation', models.CharField(max_length=10)),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apartment_bookings', to='apartment.apartment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apartment_bookings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'apartment booking',
                'verbose_name_plural': 'apartment bookings',
            },
        ),
    ]
