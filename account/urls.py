from account.views import UserRegistrationView, UserLoginView
from django.urls import path, include

app_name = "account"

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name='login'),
]
