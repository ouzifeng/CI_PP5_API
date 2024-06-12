from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.contrib.auth import get_user_model
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.authtoken.models import Token
from .serializers import CustomUserSerializer
from .email import send_password_reset_email, send_verification_email
from .models import CustomUser

User = get_user_model()


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Create a new user",
        request_body=CustomUserSerializer,
        responses={201: "User created successfully", 400: "Bad request"}
    )
    def post(self, request):
        reg_serializer = CustomUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            new_user = reg_serializer.save(is_active=False)
            if new_user:
                send_verification_email(new_user, request)
                return Response(status=status.HTTP_201_CREATED)
        return Response(
            reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


@swagger_auto_schema(
    method='post',
    operation_description="Send a contact email",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'message': openapi.Schema(type=openapi.TYPE_STRING)
        }
    ),
    responses={200: "Email sent successfully", 500: "Internal server error"}
)
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
        return Response(
            {"message": "Email sent successfully"},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@swagger_auto_schema(
    method='post',
    operation_description="Request password reset",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING)
        }
    ),
    responses={
        200: "Password reset email sent",
        400: "User with this email does not exist",
        400: "Email is not provided"
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def custom_password_reset_request(request):
    email = request.data.get('email')
    if email:
        try:
            user = User.objects.get(email=email)
            send_password_reset_email(request, user)
            return Response(
                {"message": "Password reset email sent."},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User with this email does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )
    return Response(
        {"error": "Email is not provided."},
        status=status.HTTP_400_BAD_REQUEST
    )


@swagger_auto_schema(
    method='post',
    operation_description="Confirm password reset",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'uid': openapi.Schema(type=openapi.TYPE_STRING),
            'token': openapi.Schema(type=openapi.TYPE_STRING),
            'new_password1': openapi.Schema(type=openapi.TYPE_STRING),
            'new_password2': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={
        200: "Password has been reset successfully",
        400: "Invalid token",
        400: "Passwords do not match",
        400: "Invalid UID"
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    try:
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        new_password1 = request.data.get('new_password1')
        new_password2 = request.data.get('new_password2')

        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if not default_token_generator.check_token(user, token):
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_password1 != new_password2:
            return Response(
                {"error": "Passwords do not match"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password1)
        user.save()

        return Response(
            {"message": "Password has been reset successfully"},
            status=status.HTTP_200_OK
        )
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response(
            {"error": "Invalid UID"},
            status=status.HTTP_400_BAD_REQUEST
        )


@swagger_auto_schema(
    method='get',
    operation_description="Verify email",
    manual_parameters=[
        openapi.Parameter(
            'uidb64',
            openapi.IN_PATH,
            description="UID encoded in base64",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'token',
            openapi.IN_PATH,
            description="Verification token",
            type=openapi.TYPE_STRING
        )
    ],
    responses={
        200: "Email verified successfully",
        400: "Verification link is invalid",
        400: "Invalid request"
    }
)
@api_view(['GET'])
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)

        if user and default_token_generator.check_token(user, token):
            user.email_verified = True
            user.is_active = True
            user.save()
            return Response(
                {"message": "Email verified successfully"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Verification link is invalid"},
                status=status.HTTP_400_BAD_REQUEST
            )
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        return Response(
            {"error": "Invalid request"},
            status=status.HTTP_400_BAD_REQUEST
        )


class GoogleSignIn(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Sign in with Google",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'token': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            200: openapi.Response(
                description="Google sign in successful",
                examples={
                    "application/json": {
                        'token': 'string',
                        'user_id': 'integer',
                        'first_name': 'string',
                        'last_name': 'string',
                        'email': 'string',
                        'avatar_url': 'string'
                    }
                }
            ),
            400: "Invalid token",
            400: "Google email not verified"
        }
    )
    def post(self, request):
        token = request.data.get('token')
        try:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), settings.GOOGLE_CLIENT_ID
            )
            email = idinfo['email']
            if idinfo.get('email_verified'):
                user, created = CustomUser.objects.get_or_create(
                    email=email, defaults={
                        'first_name': idinfo.get('given_name', ''),
                        'last_name': idinfo.get('family_name', ''),
                        'is_active': True,
                    }
                )

                user.avatar_url = idinfo.get('picture', '')
                if created:
                    user.set_unusable_password()
                user.save()

                token, _ = Token.objects.get_or_create(user=user)

                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'avatar_url': user.avatar_url,
                })
            else:
                return Response(
                    {"error": "Google email not verified"},
                    status=400
                )
        except ValueError:
            return Response({"error": "Invalid token"}, status=400)
