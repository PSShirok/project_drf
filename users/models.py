from django.contrib.auth.models import AbstractUser


from django.db import models

NULLBALE = {'blank': True, 'null': True}


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='users/', **NULLBALE)
    phone = models.CharField(max_length=30, **NULLBALE)
    city = models.CharField(max_length=30, **NULLBALE)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name, self.last_name}'


