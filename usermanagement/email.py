from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings


def send_password_reset_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    
    # Print user and token information
    print(f"Sending password reset email to: {user.email}")
    print(f"UID: {uid}")
    print(f"Token: {token}")
    print(f"User's last login: {user.last_login}")
    print(f"User's password hash: {user.password}")
    
    # Construct the password reset URL on the frontend
    password_reset_url = f"{settings.FRONTEND_BASE_URL}/reset-password/{uid}/{token}"


    subject = "Password Reset Requested"
    message = f"""
    Hi,

    You're receiving this email because you requested a password reset for your user account.

    Please go to the following link to set a new password:
    {password_reset_url}

    If you did not request this, please ignore this email, and your password will remain unchanged.

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
    verification_link = request.build_absolute_uri(reverse('verify-email', args=[uid, token]))
    
    subject = 'Verify your email'
    message = f'Please click the following link to verify your email: {verification_link}'
    from_email = 'mr.davidoak@gmail.com'
    recipient_list = [user.email]
    
    send_mail(subject, message, from_email, recipient_list)