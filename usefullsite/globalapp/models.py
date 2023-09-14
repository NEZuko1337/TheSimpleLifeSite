from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    img = models.ImageField(blank=True, upload_to='profile_pictures')
    
    
