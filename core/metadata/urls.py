from django.urls import path
from metadata.views import MetaDataView

urlpatterns = [
    path('metadata/', MetaDataView.as_view())
]
