from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=100)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"