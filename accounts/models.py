from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


VARN = [('BMH', 'Bramhan'),('KSH', 'Kshatriya'),('VSH', 'Vaishya'),('SDH', 'Sudra')]

class UserManager(BaseUserManager):

    def create_user(self, email, mobile, password, **other_fields):
        user = self.model(email=email, mobile=mobile, **other_fields)
        user.set_password(password)
        user.save(self._db)

        return user

    def create_superuser(self, email, mobile, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, mobile, password, **other_fields)


class Manushya(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=10, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    mobile = models.CharField(max_length=10, unique=True)
    varn = models.CharField(max_length=3, choices=VARN, default='SDH')
    hexcode = models.CharField(max_length=6, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.mobile
