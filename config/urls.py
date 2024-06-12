from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from stockdata.views import (
    StockDetailView, toggle_follow_stock, NoteListCreate,
    NoteDetail, FollowedStocksView, StockSearchView,
    DividendDataListView
)

schema_view = get_schema_view(
   openapi.Info(
      title="Your API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@yourapi.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        'api/stocks/<str:uid>/',
        StockDetailView.as_view(),
        name='stock_detail'
    ),
    path('auth/', include('dj_rest_auth.urls')),
    path('api/user/', include('usermanagement.urls')),
    path(
        'api/stocks/<str:uid>/toggle_follow/',
        toggle_follow_stock,
        name='toggle_follow_stock'
    ),
    path(
        'api/notes/',
        NoteListCreate.as_view(),
        name='note-list-create'
    ),
    path(
        'api/notes/<int:pk>/',
        NoteDetail.as_view(),
        name='note-detail'
    ),
    path(
        'api/followed_stocks/',
        FollowedStocksView.as_view(),
        name='followed-stocks'
    ),
    path(
        'api/search_stocks/',
        StockSearchView.as_view(),
        name='stock-search'
    ),
    path(
        'api/dividend_data/',
        DividendDataListView.as_view(),
        name='dividend-data-list'
    ),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc-ui'
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
