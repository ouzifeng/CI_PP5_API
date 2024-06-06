from django.urls import path
from .views import (
    CustomUserCreate, send_contact_email, custom_password_reset_request,
    password_reset_confirm, verify_email, GoogleSignIn
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', CustomUserCreate.as_view(), name='register'),
    path('send-email/', send_contact_email, name='send-contact-email'),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
    path(
        'custom-password-reset/',
        custom_password_reset_request,
        name='custom_password_reset'
    ),
    path(
        'custom/auth/password/reset/confirm/',
        password_reset_confirm,
        name='password_reset_confirm'
    ),
    path(
        'verify-email/<uidb64>/<token>/',
        verify_email,
        name='verify-email'
    ),
    path('google/login/', GoogleSignIn.as_view(), name='google_login'),
]
