from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

def send_password_reset_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    
    # Construct the password reset URL
    password_reset_url = request.build_absolute_uri(
        reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
    )

    subject = "Password Reset Requested"
    message = f"""
    Hi,

    You're receiving this email because you requested a password reset for your user account.

    Please go to the following link to set a new password:
    {password_reset_url}

    If you did not request this, please ignore this email and your password will remain unchanged.

    Thanks for using our site!
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
