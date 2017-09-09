from __future__ import unicode_literals
import shortuuid
from django.db import models
import os
from django.core.validators import MinValueValidator
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from image_cropping import ImageRatioField, ImageCropField


# Create your models here.
def get_image_path(instance, filename):
    ext = filename.split('.')[-1]
    shortuuid.set_alphabet("abcdefghijklmnopqrstuvwxyz0123456789")
    filename = "%s.%s" % (shortuuid.uuid(), ext)
    return os.path.join('profilephotos', str(instance.id), filename)

def generate_username():
    shortuuid.set_alphabet("abcdefghijklmnopqrstuvwxyz0123456789")
    return shortuuid.uuid()

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        print email
        print username
        if not email:
            raise ValueError('Users must have an email address')

        username = username if username is not None else self.normalize_email(email)
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=email,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):

    username = models.CharField(
        max_length=255,
        default=generate_username,
        unique=True
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=80)
    profile_image = ImageCropField(upload_to=get_image_path, blank=True,
                                   default='profiledefault.jpg')
    profile_ratio = ImageRatioField('profile_image', '320x320')
    email_confirmed = models.BooleanField(default=False)
    course_hours = models.IntegerField(default=0)
    is_beta = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'username'

    def get_full_name(self):
        # The user is identified by their email address
        full_name = self.first_name
        full_name += ' '
        full_name += self.last_name
        return full_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __unicode__(self):    # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
