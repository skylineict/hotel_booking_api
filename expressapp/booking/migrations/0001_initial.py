# Generated by Django 4.0 on 2024-06-17 14:13

from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hotels', '__first__'),
        ('usersauth', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_id', shortuuid.django_fields.ShortUUIDField(alphabet='abcd2020', editable=False, length=8, max_length=20, prefix='bo', unique=True)),
                ('booking_status', models.CharField(choices=[('A', 'Availed'), ('B', 'Booked'), ('C1', 'Cancelled by user'), ('C2', 'Cancelled by hotel')], max_length=2)),
                ('check_in_date', models.DateTimeField()),
                ('check_out_date', models.DateTimeField()),
                ('total_guests', models.PositiveIntegerField(default=0)),
                ('total_days', models.PositiveIntegerField(default=0)),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=15)),
                ('total_rooms', models.PositiveIntegerField(default=0)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotels.hotel')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='hotels.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usersauth.customer')),
            ],
            options={
                'verbose_name_plural': 'Booking',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Reservation_id', shortuuid.django_fields.ShortUUIDField(alphabet='abcd2020', editable=False, length=8, max_length=20, prefix='room', unique=True)),
                ('check_in_date', models.DateField()),
                ('check_out_date', models.DateField()),
                ('num_adults', models.PositiveIntegerField(default=1)),
                ('num_children', models.PositiveIntegerField(default=0)),
                ('reservation_code', models.CharField(max_length=20, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotels.hotel')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotels.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usersauth.customer')),
            ],
        ),
        migrations.CreateModel(
            name='BookOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', shortuuid.django_fields.ShortUUIDField(alphabet='abcd2020', length=8, max_length=20, prefix='hot', unique=True)),
                ('paid_status', models.BooleanField(default=False)),
                ('total', models.DecimalField(decimal_places=2, default=70.9, max_digits=10)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('book_status', models.CharField(choices=[('cash', 'Cash'), ('online', 'Online'), ('coupon', 'Coupon')], default='process', max_length=200)),
                ('invoice_no', models.CharField(default='No2304', max_length=200)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='book_order', to='booking.booking')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usersauth.customer')),
            ],
            options={
                'verbose_name_plural': 'Book Orders',
            },
        ),
    ]
