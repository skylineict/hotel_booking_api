# Generated by Django 5.0.3 on 2024-04-08 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_remove_hotel_max_guests_remove_hotel_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelroom',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
