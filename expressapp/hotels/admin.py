from django.contrib import admin
from .models import Hotel,HotelLocation,HotelReview,Category,RoomType,RoomImages,Room,Facility,BookOrder

# Register your models here.


class RoomimageAdmin(admin.TabularInline):
    model = RoomImages


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomimageAdmin]
    list_display = ['hotel_id','hotel','category_image','date','type','price','available']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','category_image','category_id']


@admin.register(HotelLocation)
class HotelLocationAdmin(admin.ModelAdmin):
    list_display = ['hotel_location_id','name','category_image','date']


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['hotles_id','owner','hotel_status','features','category_image','city']


@admin.register(RoomType)
class RoomtypeAdmin(admin.ModelAdmin):
    list_display = ['room_id','name','owner',]
    


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['facility_id','name','owner',]



@admin.register(HotelReview)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewid','user','hotel','date','rating']



@admin.register(BookOrder)
class BookOrderAdmin(admin.ModelAdmin):
    list_display = ['book_id','user','paid_status','order_date','invoice_no']


