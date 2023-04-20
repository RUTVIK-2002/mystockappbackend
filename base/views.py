from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
# Create your views here.


@csrf_protect
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
            return redirect('home')
        else:
            messages.error(request, "Username or Password does not exist")

    context = {'page': page}
    return render(request, 'base/login.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def Home(request):
    return render(request, 'base/home.html')