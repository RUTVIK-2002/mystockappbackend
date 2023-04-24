from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('home/', views.Home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('stockspage/', views.stocksPage, name='stocksPage'),
    path('stockspage/<str:pk>/', views.updateStock, name='updateStock'),
    path('addStock', views.addStock, name='addStock'),
    path('deleteStock/<str:pk>/', views.deleteStock, name='deleteStock'),
    #path('updateStock/<str:pk>/', views.updateStock, name='updateStock'),
]
