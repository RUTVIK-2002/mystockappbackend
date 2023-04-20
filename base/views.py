from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.
def loginPage(request):
    #page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

    #context = {'page': page}
    return render(request, 'base/login.html')


def logoutUser(request):
    logout(request)
    return redirect('home')

def Home(request):
    return render(request, 'base/home.html')