from django.contrib import admin
from  .models import Booking, Reservation,BookOrder

# Register your models here.


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'user','hotel','booking_status','total_days','room','booking_date','check_in_date','check_out_date']


@admin.register(Reservation)
class Reservationeadmin(admin.ModelAdmin):
    list_display = ['Reservation_id','user','hotel','num_adults','created_at']



@admin.register(BookOrder)
class BookorderAdmin(admin.ModelAdmin):
    list_display = ['book_id','paid_status','total','book_status','invoice_no', 'book']

