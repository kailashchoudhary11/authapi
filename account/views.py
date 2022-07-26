from account.models import User
from account.serializers import ChangePasswordSerializer, PasswordResetEmailSerializer, PasswordResetSerializer, UserLoginSerializer, UserProfileSerializer, UserRegistrationSerialzier
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):

    def post(self, request, format=None):
        serializer = UserRegistrationSerialzier(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({"msg": "Registration Successful!", "token": token}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # login(request, user=user)
            token = get_tokens_for_user(user)
            return Response({"msg": "Login Successful!", "token": token}, status.HTTP_200_OK)
        return Response({"errors": {"non_field_errors": ["Invalid Email or Password!"]}}, status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status.HTTP_200_OK)


class ChangePasswordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        return Response({"msg": "Password Changed Successfully!"}, status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):
    def post(self, request, format=None):
        serializer = PasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"msg": "Password reset link is sent. Please check your email!"})


class PasswordResetView(APIView):
    def post(self, request, uid, token, format=None):
        serializer = PasswordResetSerializer(data=request.data, context={
            "uid": uid,
            "token": token
        })
        serializer.is_valid(raise_exception=True)
        return Response({"msg": "Password Reset Successful!"})
