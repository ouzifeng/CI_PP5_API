from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.conf import settings
from .email import send_password_reset_email
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
