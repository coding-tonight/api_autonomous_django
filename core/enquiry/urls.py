from django.urls import path
from . import views

urlpatterns = [
    path('enquires/', views.EnquiryView.as_view())
]
