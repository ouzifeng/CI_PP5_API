from django.contrib import admin
from django.urls import path, include
from stockdata.views import StockDetailView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/stocks/<str:primary_ticker>/', StockDetailView.as_view(), name='stock_detail'),
    path('auth/', include('dj_rest_auth.urls')),
]
