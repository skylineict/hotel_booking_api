from django.db import models
from usersauth.models import Manager, Customer
from shortuuid.django_fields  import ShortUUIDField
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

class HotelLocation(models.Model):
    hotel_location_id = ShortUUIDField(unique=True, length=8, prefix='hotl', max_length=20, alphabet='hoteloc23', editable=False)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='hotel_location/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)


    class Meta:
        verbose_name_plural = 'Hotel Locations'



    def category_image(self):
        return mark_safe('<img src="%s" width="40" height="40" />'% (self.image.url))

class Category(models.Model):
    category_id = ShortUUIDField(unique=True, length=8, prefix='hot', max_length=20, alphabet='asd23', editable=False)
    name = models.CharField(_("name"), max_length=300)
    image = models.ImageField(_("image"), upload_to='category')


    
    class Meta:
        verbose_name_plural = 'Categories'

   
    def category_image(self):
        return mark_safe('<img src="%s" width="40" height="40" />'% (self.image.url))

STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('disable', 'Disable'),
    ('reject', 'Reject'),
    ('in_review', 'In Review'),
    ('approved', 'Approved')
)

class Hotel(models.Model):
    hotles_id = ShortUUIDField(unique=True, length=8, prefix='hot', max_length=20, alphabet='ahel203', editable=False)
    owner = models.ForeignKey(Manager, verbose_name=_("owner"), on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(_("address"), max_length=400)
    city = models.ForeignKey(HotelLocation, on_delete=models.CASCADE)
    state = models.CharField(max_length=255)
    images = models.ImageField(upload_to='hotel-images', default='product.jpg')
    date = models.DateTimeField(auto_now_add=True, null=True)
    specifications = models.TextField(max_length=200)
    hotel_status = models.CharField(choices=STATUS_CHOICES, max_length=200, default='in_review')
    features = models.BooleanField(_("features"), default=False)
 

    
    def category_image(self):
        return mark_safe('<img src="%s" width="40" height="40" />'% (self.image.url))

class RoomType(models.Model):
    room_id = ShortUUIDField(unique=True, length=8, prefix='room', max_length=20, alphabet='rotre34', editable=False)
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(Manager, verbose_name=_("Managers"), on_delete=models.CASCADE)

    

    

class Facility(models.Model):
    facility_id = ShortUUIDField(unique=True, length=8, prefix='fac', max_length=20, alphabet='abcd2020d', editable=False)
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(Manager, verbose_name=_("Managers"), on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Facilities'

class Room(models.Model):
    room_id = ShortUUIDField(unique=True, length=8, prefix='room', max_length=20, alphabet='abcd2020', editable=False)
    room_no = models.IntegerField(unique=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms') 
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE)   
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, default=90.93)
    available = models.BooleanField(default=True) 
    available_rooms = models.CharField(max_length=200)
    room_specification = models.TextField()
    facilities = models.ManyToManyField(Facility, verbose_name=_("facilities"), related_name='rooms')
    images = models.ImageField(upload_to='room-images', default='product.jpg')
    date = models.DateTimeField(auto_now_add=True, null=True)

    
    def category_image(self):
        return mark_safe('<img src="%s" width="40" height="40" />'% (self.image.url))

    def __str__(self):
        return f"Room: {self.room_no} - ${self.price}"

    def mark_as_booked(self):
        self.available = False
        self.save()

    def mark_as_available(self):
        self.available = True
        self.save()

class RoomImages(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, related_name='room_images')
    images = models.ImageField(upload_to='room-images', default='product.jpg')
    date = models.DateTimeField(auto_now_add=True)

    
    def category_image(self):
        return mark_safe('<img src="%s" width="40" height="40" />'% (self.image.url))

    def __str__(self):
        return self.room.address

RATING_CHOICES = [
    (1, '⭐☆☆☆☆'),
    (2, '⭐⭐☆☆☆'),
    (3, '⭐⭐⭐☆☆'),
    (4, '⭐⭐⭐⭐☆'),
    (5, '⭐⭐⭐⭐⭐'),
]

class HotelReview(models.Model):
    reviewid = ShortUUIDField(unique=True, length=8, prefix='re', max_length=20, alphabet='abcd2020')
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, related_name='hotel_reviews')
    review = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(choices=RATING_CHOICES, default=1)

    def __str__(self):
        return self.review

    def get_rating(self):
        return self.rating

    class Meta:
        verbose_name_plural = 'Hotel Reviews'

ORDER_STATUS_CHOICES = (
    ('cash', 'Cash'),
    ('online', 'Online'),
    ('coupon', 'Coupon')
)

class BookOrder(models.Model):
    book_id = ShortUUIDField(unique=True, length=8, prefix='hot', max_length=20, alphabet='abcd2020')
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    paid_status = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=70.90)
    order_date = models.DateTimeField(auto_now_add=True)
    book_status = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=200, default='process')
    invoice_no = models.CharField(max_length=200, default='No2304')
    

    class Meta:
        verbose_name_plural = 'Book Orders'

    def __str__(self):
        return self.book_status
