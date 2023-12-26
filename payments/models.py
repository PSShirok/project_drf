from django.db import models

from course.models import Course, Lesson
from users.models import User, NULLBALE


# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="дата оплаты")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLBALE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLBALE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    PAYMENT_METHOD_CHOICES = [('in_cash', 'Наличные'), ('transfer', 'Перевод на счет')]
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default='cash')

    def __str__(self):
        return f'{self.user.email} - {self.date} - {self.amount}'
