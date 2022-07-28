from account.views import ChangePasswordView, PasswordResetView, SendPasswordResetEmailView, UserProfileView, UserRegistrationView, UserLoginView
from django.urls import path

app_name = "account"

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name='login'),
    path("viewprofile/", UserProfileView.as_view(), name='profile'),
    path("changepassword/", ChangePasswordView.as_view(), name="change-password"),
    path("resetemail/", SendPasswordResetEmailView.as_view(), name="reset-email"),
    path("reset/<str:uid>/<str:token>/",
         PasswordResetView.as_view(), name="reset-email"),
]
