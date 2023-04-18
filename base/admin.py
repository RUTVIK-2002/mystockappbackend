from django.contrib import admin

# Register your models here.
from .models import Stock,ticker

admin.site.register(Stock)
admin.site.register(ticker)