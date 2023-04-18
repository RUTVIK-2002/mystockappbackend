from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('stocks/', views.getStocks),
    path('stocks/<str:pk>', views.getStock),
]
