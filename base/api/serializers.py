# these are classes that take data and convert into json objects
from rest_framework.serializers import ModelSerializer
from base.models import Stock,ticker



class TickerSerializer(ModelSerializer):
    class Meta:
        model = ticker
        fields = '__all__'

class StockSerializer(ModelSerializer):
    name = TickerSerializer()
    class Meta:
        model = Stock
        fields = '__all__'

# class StockSerializer(serializers.ModelSerializer):
#     name = TickerSerializer()

#     class Meta:
#         model = Stock
#         fields = ['id', 'name', 'current_price', 'predicted_price', 'RMSE', 'updated', 'created']
