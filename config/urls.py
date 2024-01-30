from django.contrib import admin
from django.urls import path
from stockdata.views import StockDetailView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/stocks/<str:primary_ticker>/', StockDetailView.as_view(), name='stock_detail'),
]
