from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, **kwargs):

        if 'email' in kwargs:
            email = kwargs.pop("email")
            user = self.model(
                email=self.normalize_email(email), **kwargs
            )
        else:
            raise ValueError('Users must have an email')

        password = kwargs.pop('password', None)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, **kwargs):
        email = kwargs.pop("email")
        user = self.create_user(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class EmailLowerField(models.EmailField):
    def to_python(self, value):
        if value:
            return value.lower()


class User(AbstractBaseUser, PermissionsMixin):
    email = EmailLowerField('email address', unique=True, null=True)
    phone_number = PhoneNumberField(null=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    image = models.ImageField(upload_to='user', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return f'{self.pk} - {self.email}'

