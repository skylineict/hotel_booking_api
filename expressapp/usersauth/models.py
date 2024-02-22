from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from .usermanager import CustomUsermanager
from django.utils.crypto import get_random_string
from shortuuid.django_fields  import ShortUUIDField
from django.utils.safestring import mark_safe
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
#this is a models that handles all the users model 
class JsUsermanager(AbstractBaseUser):
    email = models.EmailField(_('email address'), unique=True, max_length=200)
    username = models.CharField(_('username'), max_length=150, unique=True, null=True, blank=True)
    phone = models.CharField(_('phone number'),max_length=17, unique=True, null=True, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
    objects =  CustomUsermanager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email
    


    def has_perm(self,perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        
        return True
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    


class Manager(JsUsermanager):
    managerid = ShortUUIDField(unique=True, length=8, prefix ='mgt', max_length=20,alphabet='abcd2020')
    is_manager = models.BooleanField(_('manager status'), default=False)
    phone_verified = models.BooleanField(_('phone verified'), default=False)
    otp = models.CharField(_('OTP'), max_length=6, null=True, blank=True)

    def generate_otp(self):
        managercode = "M-"
        self.otp = managercode + get_random_string(length=6, allowed_chars='1234567890')
        self.save()




class Customer(JsUsermanager):
    customerid = ShortUUIDField(unique=True, length=8, prefix ='cus', max_length=20,alphabet='abcd2020')
    email_verified = models.BooleanField(_('email verified'), default=False)
    otp = models.CharField(_('OTP'), max_length=6, null=True, blank=True)

    def generate_otp(self):
        self.otp = get_random_string(length=6, allowed_chars='1234567890')
        self.save()


GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]


STATUS = [
        ('registered', 'Registered'),
        ('unregistered', 'Unregisterd'),
        
    ]

class ManagerDatail(models.Model):
    managerprofileid = ShortUUIDField(unique=True, length=8, prefix ='mgt', max_length=20,alphabet='abcd2020')
    user = models.OneToOneField(Manager, on_delete=models.CASCADE, related_name='manager')
    city = models.CharField(max_length=100)
    Location = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    dob = models.DateField()
    Company_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=200, choices=GENDER_CHOICES)
    lastname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    profile_image = models.ImageField(upload_to='manager_profiles/', null=True, blank=True)
    Company_status =  models.CharField(max_length=200, choices=STATUS)


    class Meta:
        verbose_name = _('ManagerDatail')
        verbose_name_plural = _('ManagerDatails')

    def __str__(self):
        return self.user.username
    
    def category_image(self):
        return mark_safe('<img src="%s" width="40" height="40" />'% (self.profile_image.url))
    
@receiver(post_save, sender=Manager)
def create_manager_profile(sender, instance, created, **kwargs):
    if created:
        ManagerDatail.objects.create(user=instance)



# managers information send here



class CustomerProfile(models.Model):
    customerprofileid = ShortUUIDField(unique=True, length=8, prefix ='cus', max_length=20,alphabet='abcd2020')
    user = models.OneToOneField(Customer, on_delete=models.CASCADE,related_name='manager')
    fullname = models.CharField(max_length=300)
    Location = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=200, choices=GENDER_CHOICES)
    profile_image = models.ImageField(upload_to='manager_profiles/', null=True, blank=True)
   
    def __str__(self):
        return self.user.email
    
    def category_image(self):
        return mark_safe('<img src="%s" width="40" height="40" />'% (self.profile_image.url))
    
@receiver(post_save, sender=Customer)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        CustomerProfile.objects.create(user=instance)




class UserSetting(models.Model):
    Faceid =  models.BooleanField(default=False)
    Rememberme  =  models.BooleanField(default=False)
    Touchid =  models.BooleanField(default=False)
    logincode =  models.BooleanField(default=False)
    notifcation = models.BooleanField(default=False)


    def __str__(self):
        return self.Faceid
    


    






