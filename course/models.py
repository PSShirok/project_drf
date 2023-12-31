from django.db import models

from users.models import NULLBALE


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=30)
    preview = models.ImageField(upload_to='course/', **NULLBALE)
    description = models.TextField()
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, **NULLBALE)

    def __str__(self):
        return f'{self.name, self.description}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=30)
    preview = models.ImageField(upload_to='lessons/', **NULLBALE)
    description = models.TextField()
    url = models.URLField(max_length=200, **NULLBALE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLBALE)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, **NULLBALE)

    def __str__(self):
        return f'{self.name, self.description}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
