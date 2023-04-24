from django.forms import ModelForm
from .models import Stock,ticker
from django.contrib.auth.models import User


class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'
        #exclude = ['host', 'participants']

class TickerForm(ModelForm):
    class Meta:
        model = ticker
        fields = '__all__'