from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager

# Create your models here.

class CustomUser(AbstractUser):

    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    user_bio = models.CharField(max_length=60)
    profile_image = models.ImageField(upload_to="profile")

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
