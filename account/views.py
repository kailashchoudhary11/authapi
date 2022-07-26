from account.models import User
from account.serializers import UserLoginSerializer, UserRegistrationSerialzier
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
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
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({"msg": "Registration Successful!", "token": token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user=user)
                token = get_tokens_for_user(user)
                return Response({"msg": "Login Successful!", "token": token}, status.HTTP_200_OK)
            return Response({"errors": {"non_field_errors": ["Invalid Email or Password!"]}}, status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status.HTTP_404_NOT_FOUND)

