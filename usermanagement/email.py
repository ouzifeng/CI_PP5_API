from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def send_password_reset_email(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    password_reset_url = f"http://yourfrontend.com/reset/{uid}/{token}"

    subject = "Password reset requested"
    message = f"""
    Hi {user.username},

    You're receiving this email because you requested a password reset for your user account at our site.

    Please go to the following page and choose a new password:
    {password_reset_url}

    If you didn't request this, please ignore this email and your password will remain unchanged.

    The site team
    """

    return subject, message
