from django.db import models

from users.models import NULLBALE


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=30)
    preview = models.ImageField(upload_to='course/', **NULLBALE)
    description = models.TextField()

    def __str__(self):
        return f'{self.name, self.description}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
