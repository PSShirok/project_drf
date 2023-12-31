from django.contrib.auth.models import AbstractUser


from django.db import models
from django.utils.translation import gettext_lazy

NULLBALE = {'blank': True, 'null': True}


class UserRights(models.TextChoices):
    MODERATOR = 'moderator', gettext_lazy('moderator')
    MEMBER = 'member', gettext_lazy('member')


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='users/', **NULLBALE)
    phone = models.CharField(max_length=30, **NULLBALE)
    city = models.CharField(max_length=30, **NULLBALE)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    rights = models.CharField(max_length=9, choices=UserRights.choices, default=UserRights.MEMBER)

    def __str__(self):
        return f'{self.first_name, self.last_name}'


