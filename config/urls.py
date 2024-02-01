from django.contrib import admin
from django.urls import path, include
from stockdata.views import StockDetailView, toggle_follow_stock

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/stocks/<str:primary_ticker>/', StockDetailView.as_view(), name='stock_detail'),
    path('auth/', include('dj_rest_auth.urls')),
    path('api/user/', include('usermanagement.urls')),
    path('api/stocks/<str:primary_ticker>/toggle_follow/', toggle_follow_stock, name='toggle_follow_stock'),
]
