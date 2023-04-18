# these are classes that take data and convert into json objects
from rest_framework.serializers import ModelSerializer
from base.models import Stock


class StockSerializer(ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'
