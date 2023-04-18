from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ticker(models.Model):
    name = models.CharField(max_length=50)
    ticker = models.CharField(max_length=50)
    shifts = models.IntegerField()
    years = models.CharField(max_length=3)

    def __str__(self):
        return self.name

class Stock(models.Model):
    name = models.OneToOneField(ticker,on_delete=models.CASCADE)
    current_price = models.DecimalField(decimal_places=2, max_digits=10)
    predicted_price = models.DecimalField(decimal_places=2, max_digits=10)
    RMSE = models.DecimalField(decimal_places=2, max_digits=10)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name.name
