from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .models import Stock,ticker
from django.db.models import Q  # this helps to make multiple queries

from django.contrib.auth.decorators import login_required
from .forms import StockForm,TickerForm

import sys
sys.path.append('STOCK_APP_FINAL_YEAR/rerunner')
import rerunner


@csrf_exempt
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        #print(username,password)
        if user and user.is_superuser:
            login(request, user)
            return render(request,'base/stockname.html')
        else:
            messages.error(request, "Username or Password does not exist")

    context = {'page': page}
    return render(request, 'base/login.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def Home(request):
    return render(request, 'base/home.html')

@login_required(login_url='login')
def stocksPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    stocks = Stock.objects.filter(
        Q(name__ticker__icontains=q) | Q(name__name__icontains=q))
    # here topic__name means take name from topic and icontains is not case sensitive and if we use contains it is case sensitive
    # topics = ticker.objects.all()[0:5]
    # room_count = stocks.count()
    #room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    if not stocks.exists():
        context = {"info":True}
    else:
        context = {'stocks': stocks}

    #return render(request, 'base/home.html', context)
    return render(request, 'base/stockname.html',context)

# @login_required(login_url='login')
# def stockInfo(request,pk):
#     stock = Stock.objects.get(id=pk)
#     context = {'stock': stock}
#     return render(request, 'base/stockinfo.html', context)

@login_required(login_url='login')
def addStock(request):
    tickers = ticker.objects.all()
    form = StockForm()
    stock = None
    #if form.is_valid():
    if request.method == 'POST':
        #print("form taken")
        
        #if form.is_valid():
        #print("form is valid")
        name = request.POST.get('name')
        ticker_name = request.POST.get('ticker')
        shifts = request.POST.get('shifts')
        years = request.POST.get('years')
        current_price = request.POST.get('current_price')
        predicted_price = request.POST.get('predicted_price')
        rmse = request.POST.get('rmse')
        ticker_obj = ticker.objects.create(name=name,ticker=ticker_name,shifts=shifts,years=years)
        stock = Stock.objects.create(
            name=ticker_obj,
            current_price=current_price,
            predicted_price=predicted_price,
            RMSE=rmse
        )
        #print("got here")
        ticker_obj.save()
        #print("ticker saved")
        stock.save()
        #print("stock saved")
        p = rerunner.shifter("hello")
        #print(p)
        return redirect('stocksPage')
    context = {'form': form, 'tickers': tickers}
    return render(request, 'base/addStock.html', context)

@login_required(login_url='login')
def deleteStock(request,pk):
    tick = Stock.objects.get(id=pk)

    if request.method == 'POST':
        tick.delete()
        return redirect('stocksPage')
    return render(request, 'base/delete.html',{'obj': tick})


@login_required(login_url='login')
def updateStock(request, pk):
    context ={}
    # Get the stock object with the given primary key
    stock = Stock.objects.get(id=pk)
    print(stock.name.id)
    
    # Get all the ticker objects
    tickers = ticker.objects.all()
    
    # Create a new instance of the TickerForm with the instance of the ticker object to be updated
    form = TickerForm(instance=stock.name)
    
    if request.method == 'POST':
        # Update the form with the new data
        form = TickerForm(request.POST, instance=stock.name)
        print(stock.name)
        if form.is_valid():
            form.save()
            return redirect('stocksPage')
    else:
        form = StockForm(instance=stock)
        context = {
        'form': form,
        'id' : stock.name.id,
        'name': stock.name.name,
        'ticker': stock.name.ticker,
        'shifts': stock.name.shifts,
        'years': stock.name.years,
        'tickers': tickers
    }

    #context = {'stock': stock, 'form': form}
    return render(request, 'base/updateStock.html', context)

    