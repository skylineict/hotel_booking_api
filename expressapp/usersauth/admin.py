from django.contrib import admin
from .models import User, Manager, Customer,ManagerDatail,CustomerProfile

# Register your models here.






@admin.register(User)
class JsUsermanageradmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'phone', 'is_active', 'is_staff', 'date_joined',]
    



@admin.register(Manager)
class ManagerUser(admin.ModelAdmin):
    list_display = ['is_manager', 'phone_verified', 'otp' ]

@admin.register(ManagerDatail)
class ManagerDatailAdmin(admin.ModelAdmin):
    list_display = ['managerprofileid','user','city','Company_name','lastname','firstname','profile_image','Company_status']


@admin.register(Customer)
class CustomerUser(admin.ModelAdmin):
    list_display = ['last_name','first_name','email','username','phone','email_verified','otp']



@admin.register(CustomerProfile)
class CustomerProfileadmin(admin.ModelAdmin):
    list_display = ['customerprofileid','user','Location','profile_image',]

