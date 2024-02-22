from django.db import models
from usersauth.models import Customer
from hotels.models import Room, Hotel
from shortuuid.django_fields  import ShortUUIDField
from django.utils.translation import gettext_lazy as _

BOOKING_STATUS = (
        ('A', 'Availed'),
        ('B', 'Booked'),
        ('C1', 'Cancelled by user'),
        ('C2', 'Cancelled by hotel')
    )

class Booking(models.Model):
 
    booking_id = ShortUUIDField(unique=True, length=8, prefix='bo', max_length=20, alphabet='abcd2020', editable=False)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    booking_status = models.CharField(max_length=2, choices=BOOKING_STATUS)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    check_in_time = models.TimeField()
    check_out_time = models.TimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    total_guests = models.PositiveIntegerField(default=0)
    total_days = models.PositiveIntegerField(default=0)
    total_cost = models.DecimalField(max_digits=15, decimal_places=2)
    coupon = models.CharField(_("coupon"), max_length=200)
    total_rooms = models.PositiveIntegerField(default=0)
    booking_date = models.DateField(auto_now_add=True)


    class Meta:
        verbose_name_plural = 'Booking'

    def __str__(self):
        return f"Booking ID: {self.booking_id} - {self.user.username} at {self.hotel.name} ({self.check_in_date} to {self.check_out_date})"

class Reservation(models.Model):
    Reservation_id = ShortUUIDField(unique=True, length=8, prefix='room', max_length=20, alphabet='abcd2020', editable=False)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    num_adults = models.PositiveIntegerField(default=1)
    num_children = models.PositiveIntegerField(default=0)
    reservation_code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation ({self.reservation_code}) by {self.user.username} for {self.room} at {self.hotel} ({self.check_in_date} - {self.check_out_date})"
