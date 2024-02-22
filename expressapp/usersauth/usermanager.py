from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _



class CustomUsermanager(BaseUserManager):
    def create_user(self, email, username=None, phone=None, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    


    def create_superuser(self, email, username=None, phone=None, password=None, **extra_fields):
        user =self.create_user(email, username, phone, password, **extra_fields)
        user.is_staff = True
        user.is_admin  = True
        user.save(using=self._db)

        return user

