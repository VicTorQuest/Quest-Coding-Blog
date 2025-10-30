from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatar", blank=True, null=True)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username