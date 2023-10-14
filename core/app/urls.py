from django.urls import path

from . views import AuthView, RegisterView, ForgetPasswordView, VerifyForgetPassword

urlpatterns = [
    path('login/', AuthView.as_view()),
    path('register/', RegisterView.as_view()),
    path('forget-password/', ForgetPasswordView.as_view()),
    path('verify-otp/', VerifyForgetPassword.as_view())
]
