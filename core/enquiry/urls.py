from django.urls import path
from . views import EnquiryView

urlpatterns = [
    path('enquires/', EnquiryView.as_view())
]
