from account.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from account.utils import Util

class UserRegistrationSerialzier(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'name', 'tc', 'password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords does not match!")  
        return super().validate(attrs)
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={"input_type": "password"}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={"input_type": "password"}, write_only=True)

    class Meta:
        fields = ['password', 'password2']
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Passwords does not match!")
        print(user.password)
        user.set_password(password)
        print(user.password)
        user.save()
        return attrs

class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("Uid", uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print("Token", token)
            link = "http://localhost:3000/api/reset/" + uid + "/" + token + "/"
            print("Link", link)
            # Send Email
            data = {
                "subject": "Reset Your Password",
                "body": "Click on the link below to reset your password.\n\n" + link,
                "to": user.email, 
            }
            Util.send_email(data)
            return attrs
        except Exception:
            raise serializers.ValidationError("Account associated with given email does not exist!")

class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={"input_type": "password"}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={"input_type": "password"}, write_only=True)

    def validate(self, attrs):
        try:

            password = attrs.get("password")
            password2 = attrs.get("password2")

            if password != password2:
                raise serializers.ValidationError("Password does not match!")

            id = smart_str(urlsafe_base64_decode(self.context.get("uid")))
            user = User.objects.get(id=id)
            token = self.context.get("token")
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Token is not Valid or Expired!")
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError("Token is not Valid or Expired!")
