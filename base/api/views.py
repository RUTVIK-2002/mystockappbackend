from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Stock
from .serializers import StockSerializer
from .. import code
import pandas as pd

from django.shortcuts import get_object_or_404


@api_view(['GET'])  # we can add PUT and POST response here
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/stocks',
        'GET /api/stocks/:id'  # this gets us particular room information
    ]
    # return JsonResponse(routes,safe=False)
    # safe allows our data to convert into Json data
    return Response(routes)


@api_view(['GET'])
def getStocks(request):
    stocks = Stock.objects.all()
    # Here the rooms are objects and they cannot be used directly so we use our serializers
    #print(stocks)

    #id_queryset = Stock.objects.all().values_list('id', flat=True)
    # Convert the queryset to a list
    #id_list = list(id_queryset)
    #print(id_list)

    # many means we are serializing multiple objects
    serializer = StockSerializer(stocks, many=True)
    return Response(serializer.data)  # it gives us data in a serialized format


@api_view(['GET'])
def getStock(request, pk):
    stock = Stock.objects.get(id=pk)
    df = pd.read_csv('shifts_years_finder.csv')
    # Here the rooms are objects and they cannot be used directly so we use our serializers
    stock.name.shifts = df.at[df[df['ticker'] == stock.name.ticker].index[0], 'shifts']
    stock.name.years = df.at[df[df['ticker'] == stock.name.ticker].index[0], 'years']
    # stock.name.shifts = df['shifts'][stock.name.ticker==df['ticker']]
    # stock.name.years = df['years'][stock.name.ticker==df['ticker']]
    #stock.save()
    #print(stock.name.ticker,stock.name.shifts,stock.name.years)
    stock.current_price,stock.predicted_price,stock.RMSE = code.model_generator(str(stock.name.ticker), int(stock.name.shifts), str(stock.name.years))
    #print(stock.current_price,stock.predicted_price,stock.RMSE)
    # many means we are serializing multiple objects
    # stock.current_price = true
    # stock.predicted_price = pred
    # stock.RMSE = RMSE
    stock.save()
    serializer = StockSerializer(stock,many=False)
    return Response(serializer.data)  # it gives us data in a serialized format
