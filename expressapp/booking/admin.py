from django.contrib import admin
from  .models import Booking, Reservation

# Register your models here.


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'user','hotel','booking_status','total_days','room','booking_date']


@admin.register(Reservation)
class Reservationeadmin(admin.ModelAdmin):
    list_display = ['Reservation_id','user','hotel','num_adults','created_at']