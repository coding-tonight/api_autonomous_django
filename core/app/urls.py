from django.urls import path
from . views import AuthView, RegisterView

urlpatterns = [
    path('login/', AuthView.as_view()),
    path('register/', RegisterView.as_view())
]
