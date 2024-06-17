from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import mark_safe


def send_password_reset_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    # Construct the password reset URL on the frontend
    password_reset_url = (
        f"{settings.FRONTEND_BASE_URL}/reset-password/{uid}/{token}"
    )

    subject = "Password Reset Requested"
    message = f"""
    Hi,

    You're receiving this email because you requested a password reset for
    your user account.

    Please go to the following link to set a new password:
    {password_reset_url}

    If you did not request this, please ignore this email, and your password
    will remain unchanged.

    Thanks for using our site!
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_url = (
        f"{settings.FRONTEND_BASE_URL}api/user/verify-email/{uid}/{token}"
    )

    subject = 'Verify your email'
    message = f"""
    Hi {user.first_name},

    Please click the link below to verify your email and activate your account:
    <a href="{verification_url}">Verify Email</a>

    If you did not request this, please ignore this email.

    Thanks for using our site!
    """

    # Mark the message as safe HTML content
    html_message = mark_safe(message)

    send_mail(
        subject,
        message,  # This is the plain-text version of the message.
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
        html_message=html_message,  # This is the HTML version.
    )
