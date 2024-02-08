from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.conf import settings
from .email import send_password_reset_email, send_verification_email
from django.contrib.auth import get_user_model



class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_serializer = CustomUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            new_user = reg_serializer.save()
            if new_user:
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def send_contact_email(request):
    name = request.data.get('name')
    from_email = request.data.get('email')
    message = request.data.get('message')

    try:
        send_mail(
            subject=f"New contact from {name}",
            message=message,
            from_email=from_email,
            recipient_list=['mr.davidoak@gmail.com'],
            fail_silently=False,
        )
        return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def custom_password_reset_request(request):
    email = request.data.get('email')
    if email:
        try:
            user = User.objects.get(email=email)
            send_password_reset_email(request, user)
            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Email is not provided."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    try:
        # Decode UID and token from the request
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        new_password1 = request.data.get('new_password1')
        new_password2 = request.data.get('new_password2')

        # Decode the uidb64 to uid
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        # Check if the token is valid for the user
        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the passwords are valid and match
        if new_password1 != new_password2:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        # Set new password
        user.set_password(new_password1)
        user.save()

        return Response({"message": "Password has been reset successfully"}, status=status.HTTP_200_OK)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({"error": "Invalid UID"}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET'])
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)

        if user and default_token_generator.check_token(user, token):
            user.email_verified = True
            user.save()
            return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Verification link is invalid"}, status=status.HTTP_400_BAD_REQUEST)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
