from django.urls import path
from .views import CustomUserCreate, send_contact_email, password_reset_request
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', CustomUserCreate.as_view(), name='register'),
    path('send-email/', send_contact_email, name='send-contact-email'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]