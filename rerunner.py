import os
import django
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockapp.settings')
django.setup()

from base.models import Stock
from base import variablesetter


id_list = [stock.id for stock in Stock.objects.all()]

for i in id_list:
    stock = Stock.objects.get(id=i)
    shifts, years = variablesetter.setter(str(stock.name.ticker))
    stock.name.shifts = shifts
    stock.name.years = years
    print(stock.name.ticker,stock.name.shifts,stock.name.years)
    stock.save()