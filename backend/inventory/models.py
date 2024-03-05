from django.db import models
from django.contrib.auth.models import User
import datetime
from category.models import Category


class Inventory(models.Model):
    photo = models.ImageField(upload_to='photos/%Y/%m/')
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=100)
    vendor = models.CharField(max_length=255)
    purchase_date = models.DateField(default=datetime.date.today)
    expiry_date = models.DateField()
    

    def __str__(self):
        return f'{self.name}'
